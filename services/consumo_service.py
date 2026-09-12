"""
Consumo de los clientes integrados contra el cupo de su plan.

**No hay tabla de contadores.** Cada cifra de este módulo sale de contar
`documentos`, que es lo que de verdad se emitió. Un contador aparte sería más
rápido de leer y se desviaría de la realidad el primer día que una emisión se
guardara sin sumar, o que un `--limpiar` borrara documentos sin restarlos. Como
lo que se cobra depende de este número, se prefiere contar cada vez.

El periodo es el mes calendario en formato `AAAA-MM`, que es como se factura una
suscripción y como lo espera `facturas_plan`.

El mes de un documento se saca con `LEFT(fecha_emision, 7)` y no con `DATE_FORMAT`:
el conector de MySQL trata el `%` de `'%Y-%m'` como marcador de parámetro y la
consulta sale mal armada según qué implementación esté instalada. `LEFT` no
depende de eso y sobre un DATETIME devuelve exactamente `AAAA-MM`.
"""
from datetime import date

from database import get_many, get_one

ESTADOS_QUE_CUENTAN = ("ACEPTADO", "PENDIENTE")


def periodo_actual() -> str:
    hoy = date.today()
    return f"{hoy.year:04d}-{hoy.month:02d}"


def periodo_facturable() -> str:
    """El ultimo mes cerrado: el unico que ya se puede cobrar.

    La mensualidad se factura sobre un mes terminado, porque hasta que el mes no
    cierra no se sabe cuantos documentos emitio el cliente ni cuanto excedente
    lleva. El mes en curso siempre aparece «sin cobrar» —y lo esta—, pero no es
    algo que nadie pueda resolver todavia: contarlo como pendiente es pedir una
    accion que no existe.
    """
    hoy = date.today()
    anio, mes = (hoy.year - 1, 12) if hoy.month == 1 else (hoy.year, hoy.month - 1)
    return f"{anio:04d}-{mes:02d}"


def periodos_recientes(cantidad: int = 6) -> list:
    """Los últimos meses con actividad, del más reciente al más antiguo.

    Sale de los documentos y no de un calendario: un mes sin emisiones no se
    ofrece como filtro, porque no hay nada que ver ahí.
    """
    filas = get_many(
        "SELECT DISTINCT LEFT(fecha_emision, 7) AS periodo "
        "FROM documentos ORDER BY periodo DESC LIMIT %s", (cantidad,))
    periodos = [f["periodo"] for f in filas]
    actual = periodo_actual()
    if actual not in periodos:
        periodos.insert(0, actual)
    return periodos


def consumo_del_periodo(periodo: str) -> list:
    """Una fila por cliente integrado: cupo, consumo, excedente y estado del cobro.

    Se listan todos los clientes, incluso los que no emitieron nada: un cliente
    que pagó su plan y dejó de emitir es justo el que hay que llamar.
    """
    filas = get_many(
        "SELECT ca.cod_cliente_api, ca.nombre, ca.plan, ca.limite_mensual, ca.estado, "
        "       ca.cod_cliente, ca.ultimo_uso, c.full_name AS cliente_nombre, "
        "       e.nombre AS emisor_nombre, "
        "       COALESCE(SUM(LEFT(d.fecha_emision, 7) = %s), 0) AS emitidos, "
        "       COALESCE(SUM(LEFT(d.fecha_emision, 7) = %s "
        "                    AND d.estado = 'RECHAZADO'), 0) AS rechazados, "
        "       fp.cod_factura_plan, fp.cod_factura, f.numero_factura AS factura_numero "
        "FROM clientes_api ca "
        "LEFT JOIN customers c ON ca.cod_cliente = c.customer_id "
        "LEFT JOIN empresas e  ON ca.cod_empresa = e.cod_empresa "
        "LEFT JOIN documentos d ON d.cod_cliente_api = ca.cod_cliente_api "
        "LEFT JOIN facturas_plan fp ON fp.cod_cliente_api = ca.cod_cliente_api "
        "     AND fp.periodo = %s "
        "LEFT JOIN facturas f ON fp.cod_factura = f.cod_factura "
        "GROUP BY ca.cod_cliente_api, fp.cod_factura_plan, fp.cod_factura, f.numero_factura "
        "ORDER BY emitidos DESC, ca.nombre",
        (periodo, periodo, periodo))

    return [_con_cupo(f) for f in filas]


def _con_cupo(fila: dict) -> dict:
    """Agrega lo que se deriva del cupo: excedente, porcentaje y semáforo."""
    emitidos = int(fila.get("emitidos") or 0)
    cupo = fila.get("limite_mensual")

    if not cupo:
        fila.update(excedente=0, porcentaje=None, semaforo="SIN_TOPE")
        return fila

    excedente = max(0, emitidos - int(cupo))
    porcentaje = round(emitidos * 100 / int(cupo), 1)
    fila.update(
        excedente=excedente,
        porcentaje=porcentaje,
        # El 80 % no es decorativo: es el punto en que hay que ofrecerle al
        # cliente el plan siguiente, antes de que le rebote una emisión.
        semaforo="EXCEDIDO" if excedente else ("ALERTA" if porcentaje >= 80 else "NORMAL"),
    )
    return fila


def documentos_del_mes(cod_cliente_api: int, periodo: str = None) -> int:
    """Cuántos documentos lleva emitidos un cliente en un mes."""
    fila = get_one(
        "SELECT COUNT(*) AS n FROM documentos "
        "WHERE cod_cliente_api = %s AND LEFT(fecha_emision, 7) = %s",
        (cod_cliente_api, periodo or periodo_actual()))
    return int(fila["n"] if fila else 0)


def cupo_disponible(cliente: dict) -> dict:
    """Cuánto le queda del plan a un cliente este mes.

    Lo consultan la API antes de emitir y el panel para mostrar la barra. Un plan
    sin `limite_mensual` es ilimitado y siempre tiene cupo: `restante` viene en
    `None` porque no hay un número que devolver, no porque sea cero.
    """
    cupo = cliente.get("limite_mensual")
    emitidos = documentos_del_mes(cliente["cod_cliente_api"])

    if not cupo:
        return {"cupo": None, "emitidos": emitidos, "restante": None, "agotado": False}

    cupo = int(cupo)
    return {"cupo": cupo, "emitidos": emitidos, "restante": max(0, cupo - emitidos),
            "agotado": emitidos >= cupo}


def serie_por_cliente(cod_cliente_api: int, meses: int = 6) -> list:
    return get_many(
        "SELECT LEFT(fecha_emision, 7) AS periodo, COUNT(*) AS emitidos, "
        "       SUM(estado = 'ACEPTADO') AS aceptados, "
        "       SUM(estado = 'RECHAZADO') AS rechazados "
        "FROM documentos WHERE cod_cliente_api = %s "
        "GROUP BY periodo ORDER BY periodo DESC LIMIT %s",
        (cod_cliente_api, meses))


def serie_de_la_plataforma(meses: int = 6) -> list:
    """Documentos por mes de todos los clientes juntos: el volumen del servicio."""
    filas = get_many(
        "SELECT LEFT(fecha_emision, 7) AS periodo, COUNT(*) AS emitidos, "
        "       COUNT(DISTINCT cod_cliente_api) AS clientes "
        "FROM documentos GROUP BY periodo ORDER BY periodo DESC LIMIT %s", (meses,))
    return list(reversed(filas))


def resumen_plataforma(periodo: str = None) -> dict:
    """Las cifras de cabecera del módulo: qué tan usado está el servicio."""
    periodo = periodo or periodo_actual()

    clientes = get_one(
        "SELECT COUNT(*) AS total, SUM(estado = 'ACTIVO') AS activos "
        "FROM clientes_api") or {}
    documentos = get_one(
        "SELECT COUNT(*) AS total, "
        "       SUM(LEFT(fecha_emision, 7) = %s) AS del_periodo, "
        "       SUM(estado = 'ACEPTADO') AS aceptados, "
        "       SUM(estado = 'RECHAZADO') AS rechazados, "
        "       SUM(estado = 'PENDIENTE') AS pendientes "
        "FROM documentos", (periodo,)) or {}

    consumo = consumo_del_periodo(periodo)
    return {
        "periodo": periodo,
        "clientes_total": int(clientes.get("total") or 0),
        "clientes_activos": int(clientes.get("activos") or 0),
        "documentos_total": int(documentos.get("total") or 0),
        "documentos_periodo": int(documentos.get("del_periodo") or 0),
        "aceptados": int(documentos.get("aceptados") or 0),
        "rechazados": int(documentos.get("rechazados") or 0),
        "pendientes": int(documentos.get("pendientes") or 0),
        "excedidos": sum(1 for c in consumo if c["semaforo"] == "EXCEDIDO"),
        "en_alerta": sum(1 for c in consumo if c["semaforo"] == "ALERTA"),
        "sin_cobrar": sum(1 for c in consumo
                          if c["estado"] == "ACTIVO" and not c["cod_factura_plan"]),
    }


def ingreso_por_plan(periodo: str = None) -> list:
    """Lo que factura cada plan en un mes: de dónde sale el ingreso recurrente.

    Sale de `facturas_plan`, que es el puente entre la mensualidad cobrada y el
    cliente que la pagó. No se deduce del precio de lista del plan: un cliente
    puede haber entrado a mitad de mes o llevar excedentes, y lo que interesa es
    lo que se cobró, no lo que costaría.
    """
    return get_many(
        "SELECT c.plan, COUNT(*) AS clientes, SUM(f.total) AS total "
        "FROM facturas_plan fp "
        "    JOIN clientes_api c ON c.cod_cliente_api = fp.cod_cliente_api "
        "    JOIN facturas f     ON f.cod_factura     = fp.cod_factura "
        "WHERE fp.periodo = %s AND f.tipo_factura = 'FV' "
        "GROUP BY c.plan ORDER BY total DESC", (periodo or periodo_actual(),))


def serie_ingreso_recurrente(meses: int = 12) -> list:
    """Lo facturado en mensualidades, mes a mes. El ingreso que se repite.

    Se separa del total facturado porque no es lo mismo: el total incluye las
    implementaciones y capacitaciones, que se cobran una vez y no vuelven.
    Mezclarlas hace ver un crecimiento que el mes siguiente no está.

    Agrupa por el mes en que se **emitió** la factura, no por el periodo de
    servicio que cobra: la mensualidad de julio se factura en agosto, y como esta
    serie se dibuja junto a la de ventas totales, las dos tienen que hablar del
    mismo eje o los picos quedarían corridos un mes entre sí.
    """
    filas = get_many(
        "SELECT LEFT(f.fecha, 7) AS periodo, COUNT(*) AS clientes, "
        "       SUM(f.total) AS total "
        "FROM facturas_plan fp "
        "    JOIN facturas f ON f.cod_factura = fp.cod_factura "
        "WHERE f.tipo_factura = 'FV' "
        "GROUP BY periodo ORDER BY periodo DESC LIMIT %s", (meses,))
    return list(reversed(filas))


# ── Series por rango de fechas ──────────────────────────────────────────────
# El panel filtra por rango, no por mes, y una serie mensual no dice nada dentro
# de una ventana de siete dias. El agrupador se arma con funciones de fecha y no
# con DATE_FORMAT, por el motivo del encabezado del modulo.

GRANULARIDADES = ("dia", "semana", "mes")

_AGRUPADOR = {
    "dia":    "DATE(fecha_emision)",
    "semana": "DATE(fecha_emision - INTERVAL WEEKDAY(fecha_emision) DAY)",
    "mes":    "DATE(fecha_emision - INTERVAL (DAY(fecha_emision) - 1) DAY)",
}


def granularidad_sugerida(desde, hasta) -> str:
    """El grano con el que un rango se lee sin quedar ni plano ni ilegible.

    Quince dias por dia caben en pantalla; un anio por dia son trescientas
    sesenta y cinco barras de un pixel. Es solo el valor inicial: quien mira
    puede cambiarlo, y por eso `granularidades_utiles` dice cuales tienen
    sentido para ese rango.
    """
    dias = (date.fromisoformat(str(hasta)) - date.fromisoformat(str(desde))).days
    if dias <= 21:
        return "dia"
    if dias <= 120:
        return "semana"
    return "mes"


def granularidades_utiles(desde, hasta) -> list:
    """Las opciones que vale la pena ofrecer para un rango.

    Se descarta el grano que daria un solo punto —un mes dentro de una ventana
    de siete dias— y el que daria cientos: una grafica de un punto no es una
    grafica, y una de trescientas barras tampoco.
    """
    dias = (date.fromisoformat(str(hasta)) - date.fromisoformat(str(desde))).days
    opciones = []
    if dias <= 120:
        opciones.append("dia")
    if 7 <= dias <= 400:
        opciones.append("semana")
    if dias >= 45:
        opciones.append("mes")
    return opciones or ["dia"]


def serie_documentos(desde, hasta, granularidad: str = None) -> dict:
    """Documentos emitidos dentro del rango, agrupados por dia, semana o mes."""
    granularidad = (granularidad if granularidad in GRANULARIDADES
                    else granularidad_sugerida(desde, hasta))
    filas = get_many(
        f"SELECT {_AGRUPADOR[granularidad]} AS periodo, COUNT(*) AS emitidos, "
        "       COUNT(DISTINCT cod_cliente_api) AS clientes "
        "FROM documentos "
        "WHERE DATE(fecha_emision) BETWEEN %s AND %s "
        "GROUP BY periodo ORDER BY periodo", (str(desde), str(hasta)))
    return {"granularidad": granularidad, "puntos": filas}


def resumen_del_rango(desde, hasta) -> dict:
    """Lo emitido dentro del rango: volumen, clientes que emitieron y aceptacion.

    Es el gemelo de `resumen_plataforma` para un rango de fechas. Aquel cuenta
    sobre todo lo historico y sobre el mes calendario, que es lo que necesita el
    modulo de consumo; el panel filtra por rango y necesitaba que sus cifras se
    movieran con el filtro.
    """
    fila = get_one(
        "SELECT COUNT(*) AS emitidos, "
        "       COUNT(DISTINCT cod_cliente_api) AS clientes, "
        "       SUM(estado = 'ACEPTADO')  AS aceptados, "
        "       SUM(estado = 'RECHAZADO') AS rechazados, "
        "       SUM(estado = 'PENDIENTE') AS pendientes "
        "FROM documentos "
        "WHERE DATE(fecha_emision) BETWEEN %s AND %s",
        (str(desde), str(hasta))) or {}
    aceptados = int(fila.get("aceptados") or 0)
    rechazados = int(fila.get("rechazados") or 0)
    resueltos = aceptados + rechazados
    return {
        "emitidos": int(fila.get("emitidos") or 0),
        "clientes": int(fila.get("clientes") or 0),
        "aceptados": aceptados,
        "rechazados": rechazados,
        "pendientes": int(fila.get("pendientes") or 0),
        # Sobre lo resuelto, no sobre lo emitido: un lote todavia en proceso no
        # es un rechazo y no tiene por que hacer caer la cifra.
        "aceptacion": round(aceptados / resueltos * 100, 1) if resueltos else None,
    }


def ingreso_recurrente_del_rango(desde, hasta) -> dict:
    """Mensualidades facturadas dentro del rango, y su reparto por plan."""
    total = get_one(
        "SELECT COUNT(*) AS mensualidades, COALESCE(SUM(f.total), 0) AS total "
        "FROM facturas_plan fp JOIN facturas f ON f.cod_factura = fp.cod_factura "
        "WHERE f.tipo_factura = 'FV' AND DATE(f.fecha) BETWEEN %s AND %s",
        (str(desde), str(hasta))) or {}
    por_plan = get_many(
        "SELECT c.plan, COUNT(*) AS clientes, SUM(f.total) AS total "
        "FROM facturas_plan fp "
        "    JOIN clientes_api c ON c.cod_cliente_api = fp.cod_cliente_api "
        "    JOIN facturas f     ON f.cod_factura     = fp.cod_factura "
        "WHERE f.tipo_factura = 'FV' AND DATE(f.fecha) BETWEEN %s AND %s "
        "GROUP BY c.plan ORDER BY total DESC", (str(desde), str(hasta)))
    return {
        "total": float(total.get("total") or 0),
        "mensualidades": int(total.get("mensualidades") or 0),
        "por_plan": por_plan,
    }
