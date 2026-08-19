"""
Consumo y facturación de planes.

Son dos preguntas de la misma conversación —cuánto emitió cada cliente este mes y
si ya se le cobró—, así que están en una sola pantalla en vez de dos. Separarlas
obligaría a mirar el consumo aquí, memorizar el número e ir a facturar allá.

Del cobro se encarga `services/facturacion_planes.py`, que emite llamando a
nuestra propia API. Esta ruta solo pregunta y muestra.
"""
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from services import consumo_service, facturacion_planes, listados
from services.api_key_service import PLANES
from services.autoservicio_client import AutoservicioError, configurado
from services.facturacion_planes import SinFacturarError
from templates_config import templates

router = APIRouter(prefix="/consumo")


@router.get("", name="consumo")
def consumo(request: Request, periodo: str = "", q: str = "", plan: str = "",
            cobro: str = "", pagina: int = 1):
    periodos = consumo_service.periodos_recientes(12)
    periodo = periodo if periodo in periodos else periodos[0]

    aviso = request.session.pop("aviso_plan", None)

    todos = consumo_service.consumo_del_periodo(periodo)
    filas = listados.buscar(todos, q, ("nombre", "cliente_nombre", "emisor_nombre"))
    filas = listados.igual_a(filas, "plan", plan)
    if cobro == "pendiente":
        filas = [f for f in filas if not f["cod_factura_plan"]]
    elif cobro == "cobrado":
        filas = [f for f in filas if f["cod_factura_plan"]]
    elif cobro == "alerta":
        filas = [f for f in filas if f["semaforo"] in ("ALERTA", "EXCEDIDO")]

    pagina_filas, meta = listados.paginar(filas, pagina)
    filtros = {"periodo": periodo, "q": q, "plan": plan, "cobro": cobro}

    return templates.TemplateResponse(request, "consumo/index.html", {
        "periodo": periodo,
        "periodos": periodos,
        "clientes": pagina_filas,
        "meta": meta,
        "filtros": filtros,
        "consulta": listados.query(filtros),
        "planes": PLANES,
        "resumen": consumo_service.resumen_plataforma(periodo),
        "serie": consumo_service.serie_de_la_plataforma(6),
        "autoservicio": configurado(),
        "aviso": aviso,
    })


@router.get("/{cod_cliente_api}/{periodo}", name="mensualidad")
def mensualidad(request: Request, cod_cliente_api: int, periodo: str):
    """La cuenta antes de emitirla. Una mensualidad emitida ya gastó un número."""
    try:
        plan = facturacion_planes.preparar(cod_cliente_api, periodo)
    except SinFacturarError as e:
        request.session["aviso_plan"] = {"tipo": "error", "texto": str(e)}
        return RedirectResponse(url=f"/consumo?periodo={periodo}", status_code=303)

    return templates.TemplateResponse(request, "consumo/mensualidad.html", {
        "plan": plan,
        "autoservicio": configurado(),
        "aviso": request.session.pop("aviso_plan", None),
    })


@router.post("/{cod_cliente_api}/{periodo}/facturar", name="facturar_mensualidad")
def facturar_mensualidad(request: Request, cod_cliente_api: int, periodo: str):
    usuario = request.session.get("user", {})
    try:
        resultado = facturacion_planes.facturar(cod_cliente_api, periodo,
                                                usuario.get("cod_usuario", 1))
    except (SinFacturarError, AutoservicioError) as e:
        detalle = getattr(e, "detalle", None) or str(e)
        request.session["aviso_plan"] = {"tipo": "error", "texto": detalle}
        return RedirectResponse(url=f"/consumo/{cod_cliente_api}/{periodo}",
                                status_code=303)

    request.session["aviso_plan"] = {
        "tipo": "exito",
        "texto": f"Mensualidad {resultado['numero']} emitida por ${resultado['total']:,.0f}. "
                 f"La emitió nuestra propia API: estado {resultado['estado']}.",
    }
    return RedirectResponse(url=f"/consumo?periodo={periodo}", status_code=303)
