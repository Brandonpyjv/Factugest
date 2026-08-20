"""
Documentos emitidos por cuenta de terceros a través de la API.

Viven en `documentos` y no en `facturas`: ahí van nuestras ventas de planes, y
mezclarlas contaría las facturas de nuestros clientes como ingresos propios en el
tablero y en los reportes.

La emisión se guarda en **dos tiempos**, y es a propósito:

1. Se reserva el número y se guarda el documento como PENDIENTE, en una
   transacción que se confirma de inmediato.
2. Se transmite al proveedor —que es una llamada de red— y después se registra
   qué contestó.

Meter la transmisión dentro de la transacción dejaría bloqueada la fila del
emisor mientras se espera una respuesta de fuera, serializando todas las
emisiones de esa empresa. Y si el proceso se cae a mitad, así queda un documento
PENDIENTE que se puede consultar y reintentar, en lugar de un número quemado sin
rastro de por qué.
"""
import secrets
from datetime import date, datetime, timedelta

from database import execute_query, execute_update, get_many, get_one, transaction
from services.documento_canonico import CLAVES_EMISOR
from services.numeracion_service import reservar_numero

FORMAS_PAGO_LEGIBLES = {"CONTADO": "Contado", "CREDITO": "Crédito"}


def nuevo_id_publico() -> str:
    """Identificador que ve el cliente. No se expone el autoincremental."""
    return "doc_" + secrets.token_hex(6)


# ── Receptores ──────────────────────────────────────────────────────────────

def resolver_receptor(cod_cliente_api: int, receptor: dict, cursor=None) -> int:
    """Devuelve el receptor, creándolo si es la primera vez que se factura a él.

    Es único por (cliente API, tipo, número): el mismo comprador enviado dos
    veces se reutiliza, y cada cliente ve solo su propio padrón.
    """
    campos = ("tipo_documento", "numero_documento", "dv", "nombre", "tipo_persona",
              "regimen_tributario", "email", "telefono", "direccion", "cod_municipio")
    valores = {c: receptor.get(c) for c in campos}

    def _buscar(cur):
        cur.execute(
            "SELECT cod_receptor FROM receptores WHERE cod_cliente_api = %s "
            "AND tipo_documento = %s AND numero_documento = %s",
            (cod_cliente_api, valores["tipo_documento"], valores["numero_documento"]))
        filas = cur.fetchall()
        return filas[0]["cod_receptor"] if filas else None

    def _guardar(cur, cod):
        if cod:
            # Los datos de contacto pueden haber cambiado desde la última venta.
            cur.execute(
                "UPDATE receptores SET nombre=%s, tipo_persona=%s, regimen_tributario=%s, "
                "  email=%s, telefono=%s, direccion=%s, cod_municipio=%s, dv=%s "
                "WHERE cod_receptor = %s",
                (valores["nombre"], valores["tipo_persona"], valores["regimen_tributario"],
                 valores["email"], valores["telefono"], valores["direccion"],
                 valores["cod_municipio"], valores["dv"], cod))
            return cod
        cur.execute(
            "INSERT INTO receptores (cod_cliente_api, tipo_documento, numero_documento, "
            "  dv, nombre, tipo_persona, regimen_tributario, email, telefono, direccion, "
            "  cod_municipio, creado_en) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (cod_cliente_api, valores["tipo_documento"], valores["numero_documento"],
             valores["dv"], valores["nombre"], valores["tipo_persona"],
             valores["regimen_tributario"], valores["email"], valores["telefono"],
             valores["direccion"], valores["cod_municipio"],
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return cur.lastrowid

    if cursor is not None:
        return _guardar(cursor, _buscar(cursor))
    with transaction() as cur:
        return _guardar(cur, _buscar(cur))


def get_receptor(cod_receptor: int):
    return get_one("SELECT * FROM receptores WHERE cod_receptor = %s", (cod_receptor,))


# ── Emisión ─────────────────────────────────────────────────────────────────

def reservar_y_guardar(cliente_api: dict, tipo: str, calculo: dict, receptor: dict,
                       cufe_de, xml_de, datos: dict) -> dict:
    """Primer tiempo: reserva el número y deja el documento como PENDIENTE.

    `cufe_de` y `xml_de` son funciones que reciben el documento ya numerado y
    devuelven el CUFE y el XML. Se pasan así porque el número tiene que existir
    antes de calcularlos, y la reserva vive dentro de esta transacción: si algo
    falla después, el consecutivo se devuelve solo.
    """
    cod_empresa = cliente_api["cod_empresa"]
    plazo = int(datos.get("plazo_dias") or 0)
    fecha = datetime.now()
    vencimiento = (date.today() + timedelta(days=plazo)).strftime("%Y-%m-%d") if plazo else None

    with transaction() as cur:
        cod_receptor = resolver_receptor(cliente_api["cod_cliente_api"], receptor, cur)
        numeracion = reservar_numero(cod_empresa, tipo, cursor=cur)

        cabecera = {
            "numero": numeracion["numero"],
            "prefijo": numeracion["prefijo"],
            "consecutivo": numeracion["consecutivo"],
            "fecha_emision": fecha,
            "fecha_vencimiento": vencimiento,
        }
        cufe = cufe_de(cabecera)
        xml = xml_de({**cabecera, "cufe": cufe}, cod_receptor)

        id_publico = nuevo_id_publico()
        cur.execute(
            "INSERT INTO documentos (id_publico, cod_cliente_api, cod_empresa, "
            "  cod_receptor, tipo, prefijo, consecutivo, numero, cufe, fecha_emision, "
            "  fecha_vencimiento, forma_pago, subtotal_bruto, total_descuentos, "
            "  descripcion_descuento_factura, subtotal, "
            "  total_impuestos, total, estado, referencia_externa, observaciones, "
            "  orden_compra, proveedor_dian, xml, cod_documento_referencia, motivo_nota, "
            "  creado_en) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            "        %s, 'PENDIENTE', %s, %s, %s, %s, %s, %s, %s, %s)",
            (id_publico, cliente_api["cod_cliente_api"], cod_empresa, cod_receptor, tipo,
             numeracion["prefijo"], numeracion["consecutivo"], numeracion["numero"], cufe,
             fecha.strftime("%Y-%m-%d %H:%M:%S.%f"), vencimiento,
             datos.get("forma_pago") or "CONTADO",
             calculo["subtotal_bruto"], calculo["total_descuentos"],
             datos.get("descripcion_descuento_factura") or None, calculo["subtotal"],
             calculo["total_impuestos"], calculo["total"],
             datos.get("referencia_externa") or None, datos.get("observaciones") or None,
             datos.get("orden_compra") or None, datos.get("proveedor_dian"), xml,
             datos.get("cod_documento_referencia"), datos.get("motivo_nota") or None,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        cod_documento = cur.lastrowid

        for orden, linea in enumerate(calculo["lineas"], start=1):
            cur.execute(
                "INSERT INTO documento_lineas (cod_documento, orden, codigo, descripcion, "
                "  unidad_medida, cantidad, precio_unitario, valor_bruto, "
                "  descuento_porcentaje, descuento_valor, descripcion_descuento, subtotal, "
                "  impuesto_codigo_dian, impuesto_porcentaje, impuesto_valor) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (cod_documento, orden, linea.get("codigo"), linea["descripcion"],
                 linea.get("unidad_medida") or "94", linea["cantidad"],
                 linea["precio_unitario"], linea["valor_bruto"],
                 linea["descuento_porcentaje"], linea["descuento_valor"],
                 linea.get("descuento_descripcion"), linea["subtotal"],
                 linea.get("impuesto_codigo_dian") or "01",
                 linea["impuesto_porcentaje"], linea["impuesto_valor"]))

        _evento(cur, cod_documento, "RECIBIDO", mensaje="Documento generado y numerado")

    return {"cod_documento": cod_documento, "id_publico": id_publico,
            "numero": numeracion["numero"], "cufe": cufe,
            "fecha_emision": fecha, "fecha_vencimiento": vencimiento,
            "cod_receptor": cod_receptor, "xml": xml}


def registrar_transmision(cod_documento: int, respuesta) -> str:
    """Segundo tiempo: guarda qué contestó el proveedor.

    Si el proveedor devolvió su propio número, CUFE o XML —Factus asigna
    numeración y firma el XML—, mandan los suyos.
    """
    estado = respuesta.estado
    campos = ["estado = %s", "proveedor_dian = %s"]
    valores = [estado, respuesta.proveedor]

    for columna, valor in (("numero", respuesta.numero), ("cufe", respuesta.cufe),
                           ("xml", respuesta.xml), ("qr", respuesta.qr)):
        if valor:
            campos.append(f"{columna} = %s")
            valores.append(valor)

    valores.append(cod_documento)
    with transaction() as cur:
        cur.execute(f"UPDATE documentos SET {', '.join(campos)} WHERE cod_documento = %s",
                    tuple(valores))
        _evento(cur, cod_documento, estado, proveedor=respuesta.proveedor,
                codigo=respuesta.codigo, mensaje=respuesta.mensaje,
                payload=respuesta.payload)
    return estado


def _evento(cursor, cod_documento, tipo, proveedor=None, codigo=None, mensaje=None,
            payload=None):
    import json
    cursor.execute(
        "INSERT INTO documento_eventos (cod_documento, tipo, proveedor, codigo, mensaje, "
        "  payload, fecha) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (cod_documento, tipo, proveedor, codigo, mensaje,
         json.dumps(payload, ensure_ascii=False, default=str) if payload else None,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))


def registrar_evento(cod_documento: int, tipo: str, **kwargs):
    with transaction() as cur:
        _evento(cur, cod_documento, tipo, **kwargs)


# ── Consulta ────────────────────────────────────────────────────────────────

def get_documento(id_publico: str, cod_cliente_api: int = None):
    """Un cliente solo puede ver sus propios documentos.

    `anulado` se deriva de que exista una nota crédito total que lo referencie, y
    no de una columna que se marque al anular. `estado` guarda lo que contestó la
    DIAN sobre *este* documento, y un documento aceptado sigue aceptado aunque
    después se anule: pisarlo con «ANULADO» borraría el hecho de que fue validado.
    """
    consulta = ("SELECT d.*, e.nombre AS empresa_nombre, "
                "       o.numero AS numero_referencia, o.cufe AS cufe_referencia, "
                "       o.fecha_emision AS fecha_referencia, "
                "       o.id_publico AS id_referencia, "
                "       EXISTS(SELECT 1 FROM documentos nc "
                "              WHERE nc.cod_documento_referencia = d.cod_documento "
                "                AND nc.tipo = 'NC' "
                "                AND nc.total >= d.total) AS anulado "
                "FROM documentos d "
                "LEFT JOIN empresas e   ON d.cod_empresa = e.cod_empresa "
                "LEFT JOIN documentos o ON d.cod_documento_referencia = o.cod_documento "
                "WHERE d.id_publico = %s")
    params = [id_publico]
    if cod_cliente_api is not None:
        consulta += " AND d.cod_cliente_api = %s"
        params.append(cod_cliente_api)
    return get_one(consulta, tuple(params))


def get_documento_por_referencia(cod_cliente_api: int, referencia: str):
    if not referencia:
        return None
    return get_one(
        "SELECT * FROM documentos WHERE cod_cliente_api = %s AND referencia_externa = %s",
        (cod_cliente_api, referencia))


def buscar_documentos(filtros: dict, limite: int = 50, desplazamiento: int = 0):
    """Documentos transmitidos, para el panel.

    A diferencia de `get_documento`, esto no filtra por cliente: es la vista del
    proveedor, que tiene que poder rastrear cualquier documento que salió por su
    infraestructura cuando un integrador llama a preguntar por uno.
    """
    donde, params = _condiciones(filtros)
    return get_many(
        "SELECT d.cod_documento, d.id_publico, d.tipo, d.numero, d.cufe, d.estado, "
        "       d.fecha_emision, d.total, d.referencia_externa, d.proveedor_dian, "
        "       ca.nombre AS cliente_nombre, ca.cod_cliente_api, "
        "       e.nombre AS emisor_nombre, e.nit AS emisor_nit, "
        "       r.nombre AS receptor_nombre, r.numero_documento AS receptor_documento "
        "FROM documentos d "
        "JOIN clientes_api ca ON d.cod_cliente_api = ca.cod_cliente_api "
        "JOIN empresas e      ON d.cod_empresa = e.cod_empresa "
        "JOIN receptores r    ON d.cod_receptor = r.cod_receptor "
        f"{donde} ORDER BY d.fecha_emision DESC, d.cod_documento DESC "
        "LIMIT %s OFFSET %s", tuple(params) + (limite, desplazamiento))


def contar_documentos(filtros: dict) -> int:
    donde, params = _condiciones(filtros)
    fila = get_one(
        "SELECT COUNT(*) AS n FROM documentos d "
        "JOIN clientes_api ca ON d.cod_cliente_api = ca.cod_cliente_api "
        "JOIN receptores r    ON d.cod_receptor = r.cod_receptor " + donde,
        tuple(params))
    return int(fila["n"] if fila else 0)


def totales_por_estado(filtros: dict) -> dict:
    donde, params = _condiciones(filtros)
    filas = get_many(
        "SELECT d.estado, COUNT(*) AS n FROM documentos d "
        "JOIN clientes_api ca ON d.cod_cliente_api = ca.cod_cliente_api "
        "JOIN receptores r    ON d.cod_receptor = r.cod_receptor "
        f"{donde} GROUP BY d.estado", tuple(params))
    return {f["estado"]: int(f["n"]) for f in filas}


def _condiciones(filtros: dict):
    """Traduce los filtros del panel a un WHERE. Vacío = todo."""
    condiciones, params = [], []

    if filtros.get("cod_cliente_api"):
        condiciones.append("d.cod_cliente_api = %s")
        params.append(int(filtros["cod_cliente_api"]))
    if filtros.get("tipo"):
        condiciones.append("d.tipo = %s")
        params.append(filtros["tipo"])
    if filtros.get("estado"):
        condiciones.append("d.estado = %s")
        params.append(filtros["estado"])
    if filtros.get("desde"):
        condiciones.append("d.fecha_emision >= %s")
        params.append(f"{filtros['desde']} 00:00:00")
    if filtros.get("hasta"):
        condiciones.append("d.fecha_emision <= %s")
        params.append(f"{filtros['hasta']} 23:59:59")
    if filtros.get("q"):
        # El integrador que llama pregunta por su número de venta, por el nuestro
        # o por el nombre del comprador: los tres tienen que servir para buscar.
        condiciones.append("(d.numero LIKE %s OR d.referencia_externa LIKE %s "
                           "OR d.cufe LIKE %s OR r.nombre LIKE %s)")
        patron = f"%{filtros['q']}%"
        params += [patron, patron, patron, patron]

    return ("WHERE " + " AND ".join(condiciones)) if condiciones else "", params


def get_lineas(cod_documento: int):
    return get_many("SELECT * FROM documento_lineas WHERE cod_documento = %s ORDER BY orden",
                    (cod_documento,))


def get_eventos(cod_documento: int):
    return get_many("SELECT * FROM documento_eventos WHERE cod_documento = %s "
                    "ORDER BY fecha, cod_evento", (cod_documento,))


# ── Conversión al documento canónico ────────────────────────────────────────

def a_documento_canonico(documento: dict, lineas: list, receptor: dict, emisor: dict):
    """Arma lo que esperan `pdf_service` y `xml_service`.

    Es el puente entre las tablas de la API y el contrato de
    `services/documento_canonico.py`, que hasta ahora solo se alimentaba de
    `facturas`. Gracias a ese contrato, el PDF y el XML salen iguales por los dos
    caminos sin duplicar una línea de generación.
    """
    forma_pago = documento.get("forma_pago") or "CONTADO"
    cabecera = {
        "cod_factura": documento.get("cod_documento"),
        "numero_factura": documento.get("numero"),
        "tipo_factura": documento.get("tipo") or "FV",
        "fecha": documento.get("fecha_emision"),
        "fecha_vencimiento": documento.get("fecha_vencimiento"),
        "subtotal": float(documento.get("subtotal") or 0),
        "total_descuentos": float(documento.get("total_descuentos") or 0),
        "total_impuestos": float(documento.get("total_impuestos") or 0),
        "total": float(documento.get("total") or 0),
        "cufe": documento.get("cufe"),
        "forma_pago": forma_pago,
        "observaciones": documento.get("observaciones"),
        "orden_compra": documento.get("orden_compra"),
        "nombre_vendedor": None,
        "descripcion_descuento_factura": documento.get("descripcion_descuento_factura"),
        # Solo viajan cuando el documento es una nota; el XML las ignora si no están.
        "motivo_nota": documento.get("motivo_nota"),
        "numero_referencia": documento.get("numero_referencia"),
        "cufe_referencia": documento.get("cufe_referencia"),
        "fecha_referencia": documento.get("fecha_referencia"),
        "metodo_pago_nombre": FORMAS_PAGO_LEGIBLES.get(forma_pago, forma_pago),
        "cliente_nombre": receptor.get("nombre"),
        "cliente_email": receptor.get("email"),
        "cliente_phone": receptor.get("telefono"),
        "cliente_address": receptor.get("direccion"),
        "cliente_ciudad": receptor.get("ciudad"),
        "cliente_departamento": receptor.get("departamento"),
        "cliente_cod_municipio": receptor.get("cod_municipio"),
        "document_type": receptor.get("tipo_documento"),
        "document_number": receptor.get("numero_documento"),
    }

    canonicas = [{
        "producto_nombre": l.get("descripcion"),
        "sku": l.get("codigo") or "",
        "unidad_medida": l.get("unidad_medida") or "94",
        "cantidad": float(l.get("cantidad") or 0),
        "precio_unitario": float(l.get("precio_unitario") or 0),
        "subtotal": float(l.get("subtotal") or 0),
        "descuento_porcentaje": float(l.get("descuento_porcentaje") or 0),
        "descuento_valor": float(l.get("descuento_valor") or 0),
        "descripcion_descuento": l.get("descripcion_descuento"),
        "impuesto_porcentaje": float(l.get("impuesto_porcentaje") or 0),
        "impuesto_valor": float(l.get("impuesto_valor") or 0),
        "impuesto_codigo_dian": l.get("impuesto_codigo_dian") or "01",
    } for l in lineas]

    return cabecera, canonicas, {c: (emisor or {}).get(c) for c in CLAVES_EMISOR}
