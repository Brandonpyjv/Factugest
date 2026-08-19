"""
Clientes integrados: quién puede llamar a nuestra API y con qué llave.

Hasta ahora un cliente se daba de alta por consola (`crear_cliente_api.py`), que
servía para el primero pero no para vender el servicio. Este módulo es el que
convierte la API en un producto: alta, plan, cupo, y la potestad de cortar el
servicio sin tocar la base de datos.

**La llave se muestra una sola vez.** De ella solo guardamos el hash, así que ni
nosotros podemos volver a verla. Es incómodo a propósito: una llave que el panel
pudiera mostrar cuando quisiera sería una llave que cualquiera con acceso al
panel puede copiarse.
"""
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from routes.formularios import formulario_invalido
from services import consumo_service, listados
from services.api_key_service import (CUPO_SUGERIDO, ESTADOS, PLANES,
                                      actualizar_cliente_api, cambiar_estado,
                                      crear_cliente_api, eliminar_cliente_api,
                                      get_all_clientes_api, get_cliente_api_by_id,
                                      rotar_llave, tiene_documentos,
                                      validar_cliente_api)
from services.branches import get_all_branches
from services.customer_service import get_all_customers
from services.documento_service import buscar_documentos
from templates_config import templates

router = APIRouter(prefix="/clientes-api")

PLANTILLA = "clientes_api/form.html"


def _catalogos():
    return {"empresas": get_all_branches(), "clientes": get_all_customers(),
            "planes": PLANES, "cupos_sugeridos": CUPO_SUGERIDO}


@router.get("", name="clientes_api")
def clientes_api(request: Request, q: str = "", estado: str = "", plan: str = "",
                 pagina: int = 1):
    todos = get_all_clientes_api()

    filas = listados.buscar(todos, q, ("nombre", "empresa_nombre", "empresa_nit",
                                       "cliente_nombre", "api_key_prefijo"))
    filas = listados.igual_a(filas, "estado", estado)
    filas = listados.igual_a(filas, "plan", plan)

    pagina_filas, meta = listados.paginar(filas, pagina)
    filtros = {"q": q, "estado": estado, "plan": plan}

    return templates.TemplateResponse(request, "clientes_api/index.html", {
        "clientes": pagina_filas,
        "meta": meta,
        "filtros": filtros,
        "consulta": listados.query(filtros),
        "estados": ESTADOS,
        "planes": PLANES,
        "resumen": consumo_service.resumen_plataforma(),
    })


@router.get("/nuevo", name="nuevo_cliente_api")
def nuevo_cliente_api(request: Request):
    return templates.TemplateResponse(request, PLANTILLA,
                                      {"cliente": None, **_catalogos()})


@router.post("/nuevo", name="crear_cliente_api_post")
def crear_cliente_api_post(request: Request, nombre: str = Form(...),
                           cod_empresa: str = Form(...), cod_cliente: str = Form(""),
                           plan: str = Form("BASICO"), limite_mensual: str = Form("")):
    enviado = {"nombre": nombre, "cod_empresa": cod_empresa, "cod_cliente": cod_cliente,
               "plan": plan, "limite_mensual": limite_mensual}
    v = validar_cliente_api(enviado)
    if not v.valido:
        return formulario_invalido(request, PLANTILLA, v,
                                   {"cliente": None, **_catalogos()}, enviado)

    d = v.datos
    cod, llave = crear_cliente_api(d["nombre"], d["cod_empresa"], d["cod_cliente"],
                                   d["plan"], d["limite_mensual"])
    # La llave viaja en la sesión y no en la URL: una URL queda en el historial del
    # navegador, en los registros del servidor y en el hombro del que va pasando.
    request.session["llave_nueva"] = {"cod": cod, "llave": llave}
    return RedirectResponse(url=f"/clientes-api/{cod}", status_code=303)


@router.get("/{cod_cliente_api}", name="ver_cliente_api")
def ver_cliente_api(request: Request, cod_cliente_api: int):
    cliente = get_cliente_api_by_id(cod_cliente_api)
    if not cliente:
        return RedirectResponse(url="/clientes-api", status_code=302)

    # Si se acaba de crear o rotar la llave, se muestra una vez y se borra: al
    # recargar la página ya no está, que es lo que se le promete al usuario.
    llave = request.session.pop("llave_nueva", None)
    if llave and llave.get("cod") != cod_cliente_api:
        llave = None

    periodo = consumo_service.periodo_actual()
    consumo = next((c for c in consumo_service.consumo_del_periodo(periodo)
                    if c["cod_cliente_api"] == cod_cliente_api), None)

    return templates.TemplateResponse(request, "clientes_api/detalle.html", {
        "cliente": cliente,
        "llave_nueva": (llave or {}).get("llave"),
        "consumo": consumo,
        "periodo": periodo,
        "serie": consumo_service.serie_por_cliente(cod_cliente_api),
        "ultimos": buscar_documentos({"cod_cliente_api": cod_cliente_api}, limite=8),
        "documentos_total": tiene_documentos(cod_cliente_api),
        "estados": ESTADOS,
    })


@router.get("/{cod_cliente_api}/editar", name="editar_cliente_api")
def editar_cliente_api(request: Request, cod_cliente_api: int):
    cliente = get_cliente_api_by_id(cod_cliente_api)
    if not cliente:
        return RedirectResponse(url="/clientes-api", status_code=302)
    return templates.TemplateResponse(request, PLANTILLA,
                                      {"cliente": cliente, **_catalogos()})


@router.post("/{cod_cliente_api}/editar", name="actualizar_cliente_api_post")
def actualizar_cliente_api_post(request: Request, cod_cliente_api: int,
                                nombre: str = Form(...), cod_empresa: str = Form(...),
                                cod_cliente: str = Form(""), plan: str = Form("BASICO"),
                                limite_mensual: str = Form("")):
    enviado = {"nombre": nombre, "cod_empresa": cod_empresa, "cod_cliente": cod_cliente,
               "plan": plan, "limite_mensual": limite_mensual}
    v = validar_cliente_api(enviado, cod_cliente_api=cod_cliente_api)
    if not v.valido:
        return formulario_invalido(
            request, PLANTILLA, v,
            {"cliente": get_cliente_api_by_id(cod_cliente_api), **_catalogos()}, enviado)

    d = v.datos
    actualizar_cliente_api(cod_cliente_api, d["nombre"], d["cod_empresa"],
                           d["cod_cliente"], d["plan"], d["limite_mensual"])
    return RedirectResponse(url=f"/clientes-api/{cod_cliente_api}", status_code=303)


@router.post("/{cod_cliente_api}/estado", name="cambiar_estado_cliente_api")
def cambiar_estado_cliente_api(request: Request, cod_cliente_api: int,
                               estado: str = Form(...)):
    if estado in ESTADOS:
        cambiar_estado(cod_cliente_api, estado)
    return RedirectResponse(url=f"/clientes-api/{cod_cliente_api}", status_code=303)


@router.post("/{cod_cliente_api}/rotar", name="rotar_llave_cliente_api")
def rotar_llave_cliente_api(request: Request, cod_cliente_api: int):
    """Reemplaza la llave. La anterior deja de servir en el acto.

    No hay periodo de gracia con las dos llaves vivas: rotar es lo que se hace
    cuando una llave se filtró, y dejarla funcionando «un ratito más» sería dejar
    entrar a quien la tenga justo cuando se descubrió que la tiene.
    """
    llave = rotar_llave(cod_cliente_api)
    request.session["llave_nueva"] = {"cod": cod_cliente_api, "llave": llave}
    return RedirectResponse(url=f"/clientes-api/{cod_cliente_api}", status_code=303)


@router.post("/{cod_cliente_api}/eliminar", name="eliminar_cliente_api")
def eliminar_cliente_api_post(request: Request, cod_cliente_api: int):
    try:
        eliminar_cliente_api(cod_cliente_api)
    except ValueError:
        return RedirectResponse(url=f"/clientes-api/{cod_cliente_api}", status_code=303)
    return RedirectResponse(url="/clientes-api", status_code=303)
