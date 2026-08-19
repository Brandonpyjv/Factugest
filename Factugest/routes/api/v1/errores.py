"""
Forma única de los errores de la API.

Quien se integra tiene que poder escribir **un solo** bloque de manejo de errores.
Si un 401 llega como `{"detail": {"codigo": ...}}`, un 422 como una lista de
Pydantic y un fallo inesperado como una página de traza, el integrador termina
adivinando qué le llegó según el código HTTP.

Aquí todo sale igual:

    {"detail": {"codigo": "llave_invalida", "mensaje": "...", "campo": null}}

Se conserva la envoltura `detail` porque es la que produce FastAPI de forma
nativa y la que ya consumen los clientes que existen; cambiarla por un objeto
plano sería romper el contrato de la v1 para ganar un nivel de anidación.

**El `codigo` es la parte estable.** El `mensaje` está escrito para que una
persona lo lea y puede cambiar de redacción; programar contra el texto es
programar contra algo que va a cambiar. El `campo` viene cuando el problema es de
un dato concreto de la petición.

Nada de lo que salga por aquí lleva traza ni nombres de tablas: un mensaje de
error es lo que un atacante lee gratis.
"""
import logging

from fastapi import HTTPException, Request, status
from fastapi.exception_handlers import (http_exception_handler,
                                        request_validation_exception_handler)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as HTTPExceptionStarlette

registro = logging.getLogger("factugest.api")

PREFIJO_API = "/api/"


def error(codigo_http: int, codigo: str, mensaje: str, campo: str = None) -> HTTPException:
    """Construye el error con la forma de la casa. Se lanza con `raise`."""
    detalle = {"codigo": codigo, "mensaje": mensaje}
    if campo:
        detalle["campo"] = campo
    return HTTPException(
        status_code=codigo_http,
        detail=detalle,
        headers={"WWW-Authenticate": "ApiKey"} if codigo_http == 401 else None,
    )


def _es_de_la_api(peticion: Request) -> bool:
    """Las rutas web devuelven HTML: envolverlas en JSON las dejaría ilegibles."""
    return peticion.url.path.startswith(PREFIJO_API)


def _cuerpo(codigo: str, mensaje: str, campo: str = None) -> dict:
    return {"detail": {"codigo": codigo, "mensaje": mensaje, "campo": campo}}


async def _manejar_http(peticion: Request, excepcion: HTTPException):
    if not _es_de_la_api(peticion):
        return await http_exception_handler(peticion, excepcion)

    detalle = excepcion.detail
    if isinstance(detalle, dict) and "codigo" in detalle:
        cuerpo = _cuerpo(detalle["codigo"], detalle.get("mensaje", ""),
                         detalle.get("campo"))
    else:
        # Un HTTPException levantado sin nuestro ayudante —o por Starlette, como
        # el 405 de un método equivocado— también tiene que salir con la forma.
        # Starlette pone el texto en inglés; el resto de la API contesta en
        # español y mezclar los dos idiomas se ve como un descuido.
        codigo, mensaje = _CODIGOS_POR_ESTADO.get(
            excepcion.status_code, ("error", str(detalle) if detalle else ""))
        cuerpo = _cuerpo(codigo, mensaje)
    return JSONResponse(status_code=excepcion.status_code, content=cuerpo,
                        headers=excepcion.headers)


async def _manejar_validacion(peticion: Request, excepcion: RequestValidationError):
    """Traduce la lista de Pydantic a un solo error con su campo señalado.

    Pydantic reporta todos los fallos; se devuelve el primero como `campo` y
    `mensaje`, y el resto se resume en el mensaje. Un integrador arregla de a un
    campo por intento de todas formas, y la lista completa obligaba a recorrer una
    estructura anidada para saber qué corregir.
    """
    if not _es_de_la_api(peticion):
        return await request_validation_exception_handler(peticion, excepcion)

    fallos = excepcion.errors()
    if not fallos:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            content=_cuerpo("datos_invalidos",
                                            "La petición no tiene la forma esperada."))

    primero = fallos[0]
    # loc[0] es «body» o «header»: al integrador le sirve la ruta dentro del cuerpo.
    ruta = ".".join(str(p) for p in primero.get("loc", [])[1:]) or None

    # Pydantic antepone «Value error, » a lo que devuelven nuestros validadores.
    # El mensaje ya está escrito para leerse; el prefijo solo delata la librería.
    mensaje = primero.get("msg", "Dato inválido")
    if mensaje.startswith("Value error, "):
        mensaje = mensaje[len("Value error, "):]
    if len(fallos) > 1:
        mensaje += f" (y {len(fallos) - 1} problema(s) más en la petición)"

    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content=_cuerpo("datos_invalidos", mensaje, ruta))


async def _manejar_inesperado(peticion: Request, excepcion: Exception):
    """Lo que nadie previó. Se registra completo y se cuenta a medias.

    La traza va al log del servidor, que es de quien la puede leer y arreglar; al
    cliente le llega que falló y con qué código puede reportarlo.
    """
    if not _es_de_la_api(peticion):
        raise excepcion

    registro.exception("Fallo no controlado en %s %s", peticion.method,
                       peticion.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_cuerpo("error_interno",
                        "Ocurrió un error inesperado procesando la petición. "
                        "Si se repite, repórtalo con la fecha y hora."))


_CODIGOS_POR_ESTADO = {
    401: ("no_autenticado", "Esta operación necesita una llave válida en X-API-Key."),
    403: ("prohibido", "La llave no tiene permiso para esta operación."),
    404: ("no_encontrado", "No existe esa ruta o ese recurso."),
    405: ("metodo_no_permitido", "Ese método HTTP no aplica a esta ruta."),
    409: ("conflicto", "La operación choca con el estado actual del recurso."),
    429: ("demasiadas_peticiones", "Demasiadas peticiones seguidas. Espera un momento."),
    500: ("error_interno", "Ocurrió un error inesperado procesando la petición."),
    502: ("proveedor_no_disponible", "No se pudo contactar al proveedor DIAN."),
}


def registrar_manejadores(app):
    """Se llama una vez al armar la aplicación.

    Se registra la excepción de Starlette y no la de FastAPI: la primera es la
    madre de la segunda, y es la que levanta el propio enrutador cuando la ruta no
    existe o el método no corresponde. Registrando solo la de FastAPI, un 404 de
    la API saldría con la forma vieja.
    """
    app.add_exception_handler(HTTPExceptionStarlette, _manejar_http)
    app.add_exception_handler(RequestValidationError, _manejar_validacion)
    app.add_exception_handler(Exception, _manejar_inesperado)
