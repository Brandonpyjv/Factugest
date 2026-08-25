"""
La mensualidad del plan: lo que le cobramos a cada cliente integrado.

Es la única parte del sistema donde las dos zonas de la base se tocan, y por eso
conviene tener claro qué queda en cada lado:

* En `documentos` queda el documento electrónico, porque se emitió por la API
  igual que el de cualquier otro cliente.
* En `facturas` queda **nuestra venta**, porque el dinero sí es nuestro y el
  tablero y los reportes tienen que contarlo.
* En `facturas_plan` queda el puente: qué mes de qué cliente ya se cobró.

**Un solo número.** La factura de la mensualidad no reserva un consecutivo propio:
se queda con el que devolvió la API. Numerar dos veces la misma venta gastaría dos
números de una resolución autorizada y dejaría el PDF diciendo algo distinto de la
factura, que es exactamente lo que la DIAN rechaza.

Lo que se cobra sale del consumo real contado en `documentos`: el plan, y los
documentos que se hayan emitido por encima del cupo.
"""
from datetime import date, datetime, timedelta

from database import get_one, transaction
from services import consumo_service
from services.autoservicio_client import emitir, ping
from services.calculo_documento import calcular_documento

SKU_EXCEDENTE = "DOC-EXTRA"
PLAZO_DIAS = 15
ESTADO_PENDIENTE = 2           # pagos_factura
METODO_TRANSFERENCIA = 4       # metodos_pago


class SinFacturarError(Exception):
    """Falta algo para poder cobrar. El mensaje se le muestra a quien lo intentó."""


def _producto(sku: str):
    return get_one(
        "SELECT p.cod_producto, p.sku, p.nombre, p.precio_unitario, "
        "       COALESCE(i.porcentaje, 0) AS impuesto_porcentaje "
        "FROM productos p LEFT JOIN impuestos i ON p.cod_impuesto = i.cod_impuesto "
        "WHERE p.sku = %s AND p.activo = 1", (sku,))


def _mes_legible(periodo: str) -> str:
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    anio, mes = periodo.split("-")
    return f"{meses[int(mes) - 1]} de {anio}"


def preparar(cod_cliente_api: int, periodo: str) -> dict:
    """Qué se le va a cobrar a un cliente por un mes, sin cobrarlo todavía.

    Se calcula aparte de emitir para que la pantalla pueda mostrar la cuenta antes
    de que alguien pulse el botón: una mensualidad emitida ya gastó un número de
    la resolución y no se deshace con un «deshacer».
    """
    consumo = next((c for c in consumo_service.consumo_del_periodo(periodo)
                    if c["cod_cliente_api"] == cod_cliente_api), None)
    if not consumo:
        raise SinFacturarError("Ese cliente no existe.")

    if not consumo.get("cod_cliente"):
        raise SinFacturarError(
            f"«{consumo['nombre']}» no está asociado a ningún cliente nuestro. "
            "Asígnalo en su ficha para poder facturarle el plan.")

    plan = _producto(f"PLAN-{consumo['plan']}")
    if not plan:
        raise SinFacturarError(
            f"No hay un producto con SKU PLAN-{consumo['plan']} en el catálogo. "
            "El precio del plan sale de ahí.")

    cliente = get_one("SELECT * FROM customers WHERE customer_id = %s",
                      (consumo["cod_cliente"],))
    if not cliente:
        raise SinFacturarError("El cliente asociado ya no existe.")

    lineas = [{
        "cod_producto": plan["cod_producto"],
        "codigo": plan["sku"],
        "descripcion": f"{plan['nombre']} — {_mes_legible(periodo)}",
        "cantidad": 1,
        "precio_unitario": float(plan["precio_unitario"]),
        "descuento_porcentaje": 0,
        "impuesto_porcentaje": float(plan["impuesto_porcentaje"]),
    }]

    excedente = int(consumo.get("excedente") or 0)
    extra = _producto(SKU_EXCEDENTE) if excedente else None
    if excedente and extra:
        lineas.append({
            "cod_producto": extra["cod_producto"],
            "codigo": extra["sku"],
            "descripcion": f"{extra['nombre']} — {excedente} documentos sobre el cupo",
            "cantidad": excedente,
            "precio_unitario": float(extra["precio_unitario"]),
            "descuento_porcentaje": 0,
            "impuesto_porcentaje": float(extra["impuesto_porcentaje"]),
        })

    calculo = calcular_documento(lineas)

    return {"consumo": consumo, "cliente": cliente, "periodo": periodo,
            "periodo_legible": _mes_legible(periodo), "lineas": calculo["lineas"],
            "totales": {k: calculo[k] for k in
                        ("subtotal_bruto", "total_descuentos", "subtotal",
                         "total_impuestos", "total")},
            "excedente": excedente,
            "ya_facturado": consumo.get("cod_factura_plan") is not None,
            "factura_numero": consumo.get("factura_numero")}


def facturar(cod_cliente_api: int, periodo: str, cod_usuario: int) -> dict:
    """Emite la mensualidad por la API y la guarda como venta nuestra.

    El orden importa: primero se emite y después se guarda. Si se guardara antes,
    un fallo de la API dejaría una factura nuestra sin número real; al revés, lo
    peor que puede pasar es que el documento quede emitido y sin registrar, y
    volver a pulsar el botón lo recupera sin emitir otro gracias a la idempotencia.
    """
    plan = preparar(cod_cliente_api, periodo)
    if plan["ya_facturado"]:
        raise SinFacturarError(
            f"El periodo {periodo} de este cliente ya se facturó "
            f"({plan['factura_numero'] or 'sin número'}).")

    cliente = plan["cliente"]
    emisor = ping()["emisor"]

    peticion = {
        # Es la misma referencia que usaría cualquier integrado: si el navegador
        # manda dos veces el formulario, la segunda devuelve el documento ya
        # emitido en vez de gastar otro número.
        "referencia_externa": f"PLAN-{cod_cliente_api}-{periodo}",
        "receptor": {
            "tipo_documento": cliente["document_type"],
            "numero_documento": cliente["document_number"],
            "nombre": cliente["full_name"],
            "tipo_persona": cliente.get("tipo_persona") or "JURIDICA",
            "regimen_tributario": cliente.get("regimen_tributario") or "RESPONSABLE_IVA",
            "email": cliente.get("email") or None,
            "telefono": cliente.get("phone") or None,
            "direccion": cliente.get("address") or None,
            "cod_municipio": cliente.get("cod_municipio") or None,
        },
        "items": [{
            "codigo": l["codigo"],
            "descripcion": l["descripcion"],
            "cantidad": l["cantidad"],
            "precio_unitario": l["precio_unitario"],
            "unidad_medida": "MON" if l["codigo"].startswith("PLAN-") else "WSD",
            "impuesto": {"codigo": "01", "porcentaje": l["impuesto_porcentaje"]},
        } for l in plan["lineas"]],
        "forma_pago": "CREDITO",
        "plazo_dias": PLAZO_DIAS,
        "observaciones": f"Suscripción {plan['consumo']['plan'].title()} — "
                         f"{plan['periodo_legible']}. "
                         f"{plan['consumo']['emitidos']} documentos emitidos.",
    }

    documento = emitir(peticion)

    fecha = datetime.now()
    vencimiento = date.today() + timedelta(days=PLAZO_DIAS)
    fila = get_one("SELECT cod_documento FROM documentos WHERE id_publico = %s",
                   (documento["id"],))

    with transaction() as cur:
        cur.execute(
            "INSERT INTO facturas (fecha, fecha_vencimiento, cod_cliente, cod_usuario, "
            "  cod_empresa, cod_metodo_pago, cod_pago, total, subtotal, total_descuentos, "
            "  total_impuestos, tipo_factura, observaciones, cufe, numero_factura, "
            "  forma_pago) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'FV',%s,%s,%s,'CREDITO')",
            (fecha.strftime("%Y-%m-%d %H:%M:%S"), vencimiento.strftime("%Y-%m-%d"),
             cliente["customer_id"], cod_usuario, emisor["cod_empresa"],
             METODO_TRANSFERENCIA, ESTADO_PENDIENTE,
             documento["totales"]["total"], documento["totales"]["base_gravable"],
             documento["totales"]["descuentos"], documento["totales"]["impuestos"],
             peticion["observaciones"], documento.get("cufe"), documento["numero"]))
        cod_factura = cur.lastrowid

        for linea in plan["lineas"]:
            cur.execute(
                "INSERT INTO detalle_factura (cod_factura, cod_producto, descripcion, "
                "  cantidad, precio_unitario, subtotal, descuento_porcentaje, "
                "  descuento_valor, impuesto_porcentaje, impuesto_valor) "
                "VALUES (%s,%s,%s,%s,%s,%s,0,0,%s,%s)",
                (cod_factura, linea["cod_producto"], linea["descripcion"],
                 linea["cantidad"], linea["precio_unitario"], linea["subtotal"],
                 linea["impuesto_porcentaje"], linea["impuesto_valor"]))

        cur.execute(
            "INSERT INTO facturas_plan (cod_cliente_api, periodo, cod_factura, "
            "  cod_documento, documentos_emitidos, documentos_excedente, creado_en) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (cod_cliente_api, periodo, cod_factura,
             fila["cod_documento"] if fila else None,
             int(plan["consumo"]["emitidos"] or 0), plan["excedente"],
             fecha.strftime("%Y-%m-%d %H:%M:%S")))

    return {"cod_factura": cod_factura, "numero": documento["numero"],
            "cufe": documento.get("cufe"), "id_publico": documento["id"],
            "estado": documento.get("estado"), "total": documento["totales"]["total"]}


def pendientes(periodo: str) -> list:
    """Clientes activos con el mes sin cobrar. Es la cola de trabajo del módulo."""
    return [c for c in consumo_service.consumo_del_periodo(periodo)
            if c["estado"] == "ACTIVO" and not c["cod_factura_plan"] and c["cod_cliente"]]
