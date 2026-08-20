"""Tablero de control: consolida las métricas del negocio y del servicio.

Los datos que alimentan las gráficas se serializan aquí, no en la plantilla: MySQL
devuelve `Decimal` y `date`, que `|tojson` no sabe convertir.
"""
from datetime import date
from urllib.parse import urlencode
from typing import Optional

from fastapi import APIRouter, Request

from auth import ADMIN_ROLES
from services import consumo_service, facturacion_planes, report_service as rep
from services.invoice_service import get_dashboard_stats
from templates_config import templates

router = APIRouter()

_MESES = ["ene", "feb", "mar", "abr", "may", "jun",
          "jul", "ago", "sep", "oct", "nov", "dic"]
_MESES_LARGOS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
                 "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

# Paleta validada con el validador de accesibilidad (OKLCH: banda de luminosidad,
# piso de croma, separación bajo daltonismo y contraste sobre superficie blanca).
# Los dos primeros son la serie categórica; el resto es la rampa ordinal de una sola
# tinta para los tramos de antigüedad de cartera, que sí tienen orden natural.
SERIE_FACTURADO = "#4e73df"
SERIE_COBRADO = "#17a673"
SERIE_DOCUMENTOS = "#6f42c1"
RAMPA_ANTIGUEDAD = ["#9cb1ec", "#7a94e5", "#5877de", "#3a58c0", "#243c92"]

# `.title()` sobre el codigo del plan deja «Basico» sin tilde. Los codigos se
# guardan sin acentos a proposito —viajan por la API—, asi que la version legible
# se pone aqui, que es donde se pinta.
NOMBRE_PLAN = {"BASICO": "Básico", "PRO": "Pro", "ILIMITADO": "Ilimitado"}
NOMBRE_GRANO = {"dia": "Día", "semana": "Semana", "mes": "Mes"}

_PRESETS = {"7": 7, "15": 15, "30": 30, "90": 90, "365": 365}


def _etiqueta_periodo(valor, granularidad):
    """El punto de una serie, rotulado segun su grano.

    La semana se rotula por el lunes con que empieza y se marca como tal: sin el
    prefijo, «17/08» de una serie semanal se lee como el dia 17 y no como los
    siete dias que arrancan ahi.
    """
    if not isinstance(valor, date):
        return str(valor)
    if granularidad == "mes":
        return f"{_MESES[valor.month - 1]} {valor.year}"
    if granularidad == "semana":
        return f"sem {valor.day:02d}/{valor.month:02d}"
    return f"{valor.day:02d}/{valor.month:02d}"


def _rango_legible(desde, hasta) -> str:
    """El rango filtrado, dicho como lo diria una persona.

    «del 22 de julio al 20 de agosto de 2026», y sin repetir el anio cuando es el
    mismo en los dos extremos. Es el texto que aparece bajo cada seccion, asi que
    tiene que cambiar con el filtro: antes decia el mes calendario y se quedaba
    igual aunque se estuvieran mirando doce meses.
    """
    d = date.fromisoformat(str(desde))
    h = date.fromisoformat(str(hasta))
    if d == h:
        return f"el {d.day} de {_MESES_LARGOS[d.month - 1]} de {d.year}"
    izq = f"{d.day} de {_MESES_LARGOS[d.month - 1]}"
    if d.year != h.year:
        izq += f" de {d.year}"
    return f"del {izq} al {h.day} de {_MESES_LARGOS[h.month - 1]} de {h.year}"


def _etiqueta_mes(periodo: str) -> str:
    """`AAAA-MM` como lo escribe `consumo_service` -> «ago 2026»."""
    anio, mes = periodo.split("-")
    return f"{_MESES[int(mes) - 1]} {anio}"


def _resolver_rango(desde, hasta, preset):
    """La ventana por defecto es de un anio, no de un mes.

    FactuGest le factura a cada cliente una vez al mes. En una ventana de treinta
    dias eso da un solo punto —o ninguno, si el corte cae entre dos cobros—, y el
    tablero abria vacio aunque el negocio estuviera funcionando. Un anio muestra
    la curva de suscriptores, que es lo que hay que mirar en un servicio.
    """
    if preset in _PRESETS:
        return rep.rango_por_defecto(_PRESETS[preset])
    if desde and hasta:
        return desde, hasta
    return rep.rango_por_defecto(365)


def _resolver_empresa(request: Request, empresa_param: Optional[str]):
    """Cada usuario ve su empresa; solo ADMIN puede consolidar todas."""
    usuario = request.session.get("user", {})
    if usuario.get("rol") == "ADMIN":
        if empresa_param == "todas":
            return None
        if empresa_param:
            return int(empresa_param)
    return usuario.get("cod_empresa")


@router.get("/", name="index")
def index(request: Request, desde: str = "", hasta: str = "",
          preset: str = "", empresa: str = "", gran: str = ""):
    usuario = request.session.get("user", {})

    # El cajero no gestiona finanzas: su panel es operativo.
    if usuario.get("rol") not in ADMIN_ROLES:
        return templates.TemplateResponse(request, "dashboard/cajero.html", {
            "stats": get_dashboard_stats(),
        })

    desde, hasta = _resolver_rango(desde, hasta, preset)
    cod_empresa = _resolver_empresa(request, empresa)

    # El grano de las dos series temporales. Se ofrece el mismo a las dos para que
    # el eje de «documentos emitidos» y el de «facturacion y cobro» hablen de los
    # mismos tramos y se puedan leer una contra otra.
    granos = consumo_service.granularidades_utiles(desde, hasta)
    grano = gran if gran in granos else consumo_service.granularidad_sugerida(desde, hasta)
    if grano not in granos:
        grano = granos[0]

    kpis = rep.get_kpis(desde, hasta, cod_empresa)
    cartera = rep.get_cartera(cod_empresa)
    antiguedad = rep.get_cartera_por_antiguedad(cod_empresa)
    serie = rep.get_serie_ventas(desde, hasta, cod_empresa, granularidad=grano)

    # Las metricas del servicio, dentro del rango filtrado.
    servicio = consumo_service.resumen_del_rango(desde, hasta)
    serie_documentos = consumo_service.serie_documentos(desde, hasta, grano)
    recurrente = consumo_service.ingreso_recurrente_del_rango(desde, hasta)
    anterior = consumo_service.ingreso_recurrente_del_rango(*rep.periodo_anterior(desde, hasta))
    recurrente["variacion"] = (
        round((recurrente["total"] - anterior["total"]) / anterior["total"] * 100, 1)
        if anterior["total"] else None)

    # El cupo es la excepcion, y por eso lo dice su tarjeta: se agota por mes
    # calendario, asi que recortarlo a una ventana movil de N dias daria un consumo
    # que no corresponde con el que se le factura al cliente.
    plataforma = consumo_service.resumen_plataforma()
    consumo = consumo_service.consumo_del_periodo(plataforma["periodo"])

    # Los que mas emiten, no solo los que van pasados de cupo: la lista filtrada por
    # semaforo aparecia vacia cualquier mes en que nadie se acercara al limite, que es
    # lo normal, y el panel perdia su unica vista de quien esta usando el servicio.
    # El semaforo sigue estando, ahora como color de cada fila.
    mas_activos = [c for c in consumo if c["emitidos"]][:6]

    # La mensualidad se cobra sobre un mes terminado, no sobre el que va corriendo:
    # esta cifra mira el ultimo mes cerrado y no el rango, porque es una cola de
    # trabajo. Con el mes actual el panel decia «14 mensualidades sin cobrar» el dia
    # siguiente de haberlas cobrado todas: siempre cierto, nunca accionable.
    facturable = consumo_service.periodo_facturable()
    pendientes_de_cobro = len(facturacion_planes.pendientes(facturable))

    graficas = {
        "serie": {
            "etiquetas": [_etiqueta_periodo(p["periodo"], serie["granularidad"])
                          for p in serie["puntos"]],
            "facturado": [float(p["ventas"] or 0) for p in serie["puntos"]],
            "cobrado":   [float(p["cobrado"] or 0) for p in serie["puntos"]],
        },
        # El volumen del servicio: lo que se emitio por cuenta de los clientes.
        # Va en su propia tinta porque no es dinero, es cantidad de documentos.
        "documentos": {
            "etiquetas": [_etiqueta_periodo(f["periodo"], serie_documentos["granularidad"])
                          for f in serie_documentos["puntos"]],
            "valores":   [int(f["emitidos"] or 0) for f in serie_documentos["puntos"]],
            "clientes":  [int(f["clientes"] or 0) for f in serie_documentos["puntos"]],
        },
        "planes": {
            "etiquetas": [NOMBRE_PLAN.get(p["plan"], p["plan"].title())
                          for p in recurrente["por_plan"]],
            "valores":   [float(p["total"] or 0) for p in recurrente["por_plan"]],
        },
        "antiguedad": {
            "etiquetas": [t["tramo"] for t in antiguedad],
            "valores":   [float(t["valor"] or 0) for t in antiguedad],
            "colores":   RAMPA_ANTIGUEDAD,
        },
        "colores": {"facturado": SERIE_FACTURADO, "cobrado": SERIE_COBRADO,
                    "documentos": SERIE_DOCUMENTOS},
    }

    # Gemelo en tabla de la serie: los mismos números sin depender del tooltip.
    serie_tabla = [
        {"periodo":   graficas["serie"]["etiquetas"][i],
         "facturado": graficas["serie"]["facturado"][i],
         "cobrado":   graficas["serie"]["cobrado"][i],
         "facturas":  serie["puntos"][i]["facturas"]}
        for i in range(len(serie["puntos"]))
    ]

    return templates.TemplateResponse(request, "dashboard/index.html", {
        "kpis":          kpis,
        "cartera":       cartera,
        "antiguedad":    antiguedad,
        "serie":         serie,
        "serie_tabla":   serie_tabla,
        "plataforma":    plataforma,
        "servicio":      servicio,
        "recurrente":    recurrente,
        "mas_activos":   mas_activos,
        "nombre_plan":   NOMBRE_PLAN,
        "facturable":    _etiqueta_mes(facturable),
        "pendientes_de_cobro": pendientes_de_cobro,
        "serie_documentos": serie_documentos,
        "recientes":     get_dashboard_stats(recientes=12)["facturas_recientes"],
        "graficas":      graficas,
        "filtros":       {"desde": desde, "hasta": hasta, "preset": preset,
                          "empresa": empresa, "gran": grano},
        "rango_legible": _rango_legible(desde, hasta),
        "granos":        granos,
        "nombre_grano":  NOMBRE_GRANO,
        # El selector de grano conserva el rango: sin esto, cambiar de grano
        # devolvia al periodo por defecto y se perdia el filtro que se estaba
        # mirando.
        "consulta_base": urlencode({k: v for k, v in
                                    (("preset", preset), ("desde", desde),
                                     ("hasta", hasta), ("empresa", empresa)) if v}),
        "empresas":      rep.get_empresas_disponibles() if usuario.get("rol") == "ADMIN" else [],
        "es_admin":      usuario.get("rol") == "ADMIN",
    })
