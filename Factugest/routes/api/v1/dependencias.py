"""
Autenticación de la API de integración.

La web usa sesión con cookie y la API usa una llave por cliente. Son dos puertas
distintas al mismo sistema: `AuthMiddleware` deja pasar `/api/v1/` sin mirar la
sesión precisamente porque aquí se verifica de otra forma.

    from routes.api.v1.dependencias import ClienteAPI

    @router.post("/facturas")
    def emitir(cliente: ClienteAPI):
        cliente["cod_empresa"]   # el emisor con el que numera este cliente
"""
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from services.api_key_service import (ClienteInactivoError, LlaveInvalidaError,
                                      autenticar)


def _error(codigo_http: int, codigo: str, mensaje: str) -> HTTPException:
    """Un mismo cuerpo para todos los errores, para que el que se integra no
    tenga que interpretar cada uno a su manera. La tarea 3.5 lo extiende al
    resto de la API."""
    return HTTPException(
        status_code=codigo_http,
        detail={"codigo": codigo, "mensaje": mensaje},
        headers={"WWW-Authenticate": "ApiKey"} if codigo_http == 401 else None,
    )


def get_cliente_api(
    x_api_key: Annotated[str | None, Header(
        alias="X-API-Key",
        description="Llave del cliente integrado, con el formato fg_live_xxxx.secreto",
    )] = None,
) -> dict:
    """Resuelve el cliente dueño de la llave, o corta la petición.

    Se distingue entre no traer llave y traer una que no sirve (401) y traer una
    válida de un cliente suspendido (403): en el primer caso el que se integra
    revisa su configuración, y en el segundo tiene que hablar con nosotros.
    """
    if not x_api_key:
        raise _error(status.HTTP_401_UNAUTHORIZED, "llave_ausente",
                     "Falta el encabezado X-API-Key.")

    try:
        return autenticar(x_api_key)
    except LlaveInvalidaError:
        raise _error(status.HTTP_401_UNAUTHORIZED, "llave_invalida",
                     "La llave no es válida.")
    except ClienteInactivoError as e:
        raise _error(status.HTTP_403_FORBIDDEN, "cliente_inactivo",
                     f"El cliente está {e.estado.lower()}. Contáctanos para reactivarlo.")


# Atajo para no repetir Depends en cada endpoint.
ClienteAPI = Annotated[dict, Depends(get_cliente_api)]
