"""Siembra la operación de FactuGest como proveedor tecnológico.

    python seed_proveedor.py            # genera los datos
    python seed_proveedor.py --limpiar  # deshace exactamente lo generado

Este es **el único sembrador de FactuGest**, y siembra el negocio que FactuGest
tiene hoy: vender el servicio de facturar, no vender mercancía. Crea:

* La empresa emisora **FactuGest S.A.S.**, con su resolución de la DIAN.
* El **catálogo de servicios** (`controla_stock = 0` en todos): los tres planes,
  el documento adicional fuera del cupo, y lo que se cobra una vez al enganchar a
  un cliente —implementación, habilitación ante la DIAN, capacitación—. Aquí no
  hay teclados ni monitores: un proveedor tecnológico no tiene bodega.
* Catorce **empresas suscritas**, cada una con su fila en `customers` (a quién le
  facturamos), su fila en `empresas` (con qué NIT y resolución emite) y su fila
  en `clientes_api` (con qué llave nos llama). Entraron en meses distintos, que es
  como crece un negocio de este tipo. Siste Soluciones es una de ellas y se
  reutiliza la que ya existe, no se duplica.
* El **tráfico** de tres meses en `documentos`: lo que hemos emitido por cuenta de
  ellos. De ahí sale el consumo contra el cupo, sin tabla de contadores.
* Las **ventas** de los últimos seis meses en `facturas`: la factura de enganche de
  cada cliente y su mensualidad, que es lo que cuenta el tablero.

Dos cosas que este sembrador **no** hace, a propósito:

1. No guarda el XML de los documentos sembrados. El XML es lo que se firma y hay
   deber de conservar, pero estos documentos no se emitieron: son de mentira.
   Guardar tres mil XML inventados abultaría la base sin agregar nada a la
   demostración. Los que emite la API de verdad sí lo llevan.
2. No cobra los dos últimos meses. El mes en curso todavía no terminó, y el
   anterior queda pendiente a propósito: es el que tiene el consumo cerrado, con
   clientes que se pasaron del cupo, y es el que se factura en vivo en la
   sustentación desde el módulo de consumo.

Cada objeto creado se anota en `seed_proveedor_manifest.json` y `--limpiar` borra
exactamente eso, restaurando además los consecutivos y la empresa de los usuarios.
Es determinista: dos ejecuciones producen la misma operación.

**No usar en producción.**
"""
import argparse
import json
import os
import random
import sys
from datetime import date, datetime, timedelta

from database import execute_update, get_many, get_one, transaction
from services.api_key_service import crear_cliente_api
from services.calculo_documento import calcular_documento
from services.cufe_service import generate_cufe

# El manifiesto lleva el nombre de la base en el archivo: sembrar contra una base
# de prueba y contra la de siempre son dos operaciones distintas, y con un único
# archivo la segunda siembra creía que ya estaba hecha —o peor, `--limpiar`
# borraba en una base lo que se había creado en la otra.
_BASE = os.getenv("DB_NAME", "factugest")
MANIFIESTO = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          f"seed_proveedor_manifest.{_BASE}.json")

HOY = date(2026, 8, 19)
MESES_DE_TRAFICO = 3         # documentos emitidos por cuenta de terceros
MESES_DE_COBRO = 6           # mensualidades que ya les facturamos

SEMILLA = 20260819

# Estados de pago (tabla pagos_factura)
PAGADA, PENDIENTE, VENCIDA = 1, 2, 4
IVA = 1                      # cod_impuesto del 19 %
TRANSFERENCIA = 4            # metodos_pago: así se cobra una suscripción

EMISOR = {
    "nombre": "FactuGest S.A.S.",
    "nit": "901245678",
    "dv": "1",
    "direccion": "Av. Gran Colombia # 12-45, oficina 402",
    "ciudad": "San Jose De Cucuta",
    "cod_municipio": "54001",
    "telefono": "6075832100",
    "correo": "facturacion@factugest.co",
    "website": "factugest.co",
    "regimen_tributario": "RESPONSABLE_IVA",
    # 6201: desarrollo de sistemas informáticos. Es lo que hacemos, y va en el XML.
    "actividad_economica": "6201",
    "tipo_documento": "NIT",
    "prefijo_factura": "FG",
    "resolucion_dian": "18764002451009",
    "resolucion_desde": 1,
    "resolucion_hasta": 5000,
}

# El cupo vive aquí y en `clientes_api.limite_mensual`; el precio, en el producto.
# Subir una tarifa es editar un producto, no migrar datos.
PLANES = {
    "BASICO":    {"sku": "PLAN-BASICO",    "precio": 89000,  "cupo": 150},
    "PRO":       {"sku": "PLAN-PRO",       "precio": 189000, "cupo": 400},
    "ILIMITADO": {"sku": "PLAN-ILIMITADO", "precio": 390000, "cupo": None},
}

SKU_EXCEDENTE = "DOC-EXTRA"

# El catálogo de FactuGest son servicios, y no por elegancia: un proveedor
# tecnológico no tiene bodega. Todos van con `controla_stock = 0`, así que la
# emisión no les toca existencias y el módulo de inventario los ignora.
PRODUCTOS = [
    # sku, nombre, descripcion, precio, unidad
    ("PLAN-BASICO", "Plan Básico — 150 documentos/mes",
     "Suscripción mensual a la API de facturación electrónica. Incluye 150 documentos.",
     89000, "MON"),
    ("PLAN-PRO", "Plan Pro — 400 documentos/mes",
     "Suscripción mensual a la API de facturación electrónica. Incluye 400 documentos.",
     189000, "MON"),
    ("PLAN-ILIMITADO", "Plan Ilimitado — sin tope de documentos",
     "Suscripción mensual a la API de facturación electrónica sin límite de emisión.",
     390000, "MON"),
    (SKU_EXCEDENTE, "Documento adicional fuera del cupo",
     "Documento electrónico emitido por encima del cupo incluido en el plan.",
     250, "WSD"),
    ("IMPL-API", "Implementación e integración",
     "Conexión del sistema del cliente con la API: acompañamiento técnico, pruebas "
     "en ambiente de habilitación y puesta en producción. Se cobra una vez.",
     450000, "WSD"),
    ("HABILITACION", "Acompañamiento en la habilitación ante la DIAN",
     "Trámite de la resolución de numeración y del proceso de habilitación como "
     "facturador electrónico. Se cobra una vez.",
     250000, "WSD"),
    ("CAPACITACION", "Capacitación al equipo del cliente",
     "Sesión de formación para el personal que va a operar la facturación. "
     "Por sesión.",
     180000, "WSD"),
    ("SOPORTE-PRIORITARIO", "Soporte prioritario",
     "Canal directo con tiempo de respuesta garantizado de 4 horas hábiles. "
     "Se cobra mensual, aparte del plan.",
     120000, "MON"),
]

# Los que se cobran una sola vez, al enganchar al cliente. Sin ellos el tablero
# solo vería mensualidades idénticas mes a mes, que no es como se ve un negocio
# de este tipo: el mes que entra un cliente nuevo se factura bastante más.
SERVICIOS_DE_ENGANCHE = ["IMPL-API", "HABILITACION", "CAPACITACION"]

# Las empresas suscritas. `antiguedad` es hace cuántos meses entraron: no todas
# llevan lo mismo, porque un negocio que va sumando clientes se ve distinto de uno
# que arrancó con catorce el mismo día, y el tablero tiene que poder mostrar eso.
SUSCRIPTORES = [
    {"nombre": "Siste Soluciones S.A.S.", "nit": "901555444", "dv": "7",
     "actividad": "4741", "direccion": "C.C. Gran Bulevar, local 103",
     "telefono": "6075551234", "correo": "facturacion@sistesoluciones.com",
     "plan": "BASICO", "prefijo": "SETP", "resolucion": "18764003812345",
     "volumen": (55, 95), "estado": "ACTIVO", "antiguedad": 6},

    {"nombre": "Droguería La Salud S.A.S.", "nit": "900874512", "dv": "3",
     "actividad": "4772", "direccion": "Calle 11 # 6-32, barrio La Playa",
     "telefono": "6075742210", "correo": "administracion@drogueriaslasalud.co",
     "plan": "PRO", "prefijo": "DLS", "resolucion": "18764003812501",
     "volumen": (395, 430), "estado": "ACTIVO", "antiguedad": 6},

    {"nombre": "Ferretería Los Andes S.A.S.", "nit": "901102337", "dv": "9",
     "actividad": "4752", "direccion": "Av. 4 # 14-88, centro",
     "telefono": "6075719044", "correo": "cartera@ferreterialosandes.com",
     "plan": "PRO", "prefijo": "FLA", "resolucion": "18764003812644",
     "volumen": (200, 260), "estado": "ACTIVO", "antiguedad": 6},

    {"nombre": "Transportes del Norte S.A.S.", "nit": "890502114", "dv": "5",
     "actividad": "4921", "direccion": "Terminal de Transportes, módulo 7",
     "telefono": "6075836677", "correo": "facturacion@transportesdelnorte.co",
     "plan": "ILIMITADO", "prefijo": "TDN", "resolucion": "18764003812770",
     "volumen": (280, 340), "estado": "ACTIVO", "antiguedad": 6},

    {"nombre": "Papelería Escolar Cúcuta", "nit": "1090345678", "dv": "0",
     "actividad": "4761", "direccion": "Calle 6 # 3-21, barrio Latino",
     "telefono": "3156644821", "correo": "papeleriaescolar54@gmail.com",
     "plan": "BASICO", "prefijo": "PEC", "resolucion": "18764003812899",
     "volumen": (30, 55), "estado": "SUSPENDIDO", "antiguedad": 6},

    {"nombre": "Restaurante La Mazorca", "nit": "1090778234", "dv": "4",
     "actividad": "5611", "direccion": "Av. Libertadores # 10-56",
     "telefono": "3204471188", "correo": "lamazorcacucuta@gmail.com",
     "plan": "BASICO", "prefijo": "RLM", "resolucion": "18764003813012",
     "volumen": (60, 110), "estado": "ACTIVO", "antiguedad": 5},

    {"nombre": "Distribuidora El Establo S.A.S.", "nit": "900661209", "dv": "1",
     "actividad": "4631", "direccion": "Zona Industrial, bodega 14",
     "telefono": "6075884420", "correo": "facturacion@elestablo.com.co",
     "plan": "PRO", "prefijo": "DEE", "resolucion": "18764003813155",
     "volumen": (180, 240), "estado": "ACTIVO", "antiguedad": 5},

    {"nombre": "Taller Motor Norte", "nit": "1093822014", "dv": "6",
     "actividad": "4520", "direccion": "Av. 7 # 22-31, barrio Blanco",
     "telefono": "3115523097", "correo": "tallermotornorte@hotmail.com",
     "plan": "BASICO", "prefijo": "TMN", "resolucion": "18764003813288",
     "volumen": (25, 60), "estado": "ACTIVO", "antiguedad": 4},

    {"nombre": "Confecciones Doña Rosa", "nit": "1090114523", "dv": "8",
     "actividad": "1410", "direccion": "Calle 15 # 2-40, La Playa",
     "telefono": "3178840012", "correo": "confeccionesrosa@gmail.com",
     "plan": "BASICO", "prefijo": "CDR", "resolucion": "18764003813401",
     "volumen": (20, 45), "estado": "ACTIVO", "antiguedad": 4},

    {"nombre": "Supermercado La Economía S.A.S.", "nit": "900338177", "dv": "2",
     "actividad": "4711", "direccion": "Calle 8 # 5-12, centro",
     "telefono": "6075512233", "correo": "sistemas@laeconomia.com.co",
     "plan": "ILIMITADO", "prefijo": "SLE", "resolucion": "18764003813566",
     "volumen": (300, 380), "estado": "ACTIVO", "antiguedad": 3},

    {"nombre": "Clínica Odontológica Sonrisas", "nit": "901447903", "dv": "0",
     "actividad": "8622", "direccion": "Av. 0 # 14-22, consultorio 301",
     "telefono": "6075747711", "correo": "citas@sonrisascucuta.co",
     "plan": "BASICO", "prefijo": "COS", "resolucion": "18764003813699",
     "volumen": (35, 70), "estado": "ACTIVO", "antiguedad": 3},

    {"nombre": "Hotel Casa Blanca", "nit": "900902551", "dv": "7",
     "actividad": "5511", "direccion": "Av. 1 # 12-18, barrio Latino",
     "telefono": "6075719900", "correo": "recepcion@hotelcasablanca.co",
     "plan": "PRO", "prefijo": "HCB", "resolucion": "18764003813744",
     "volumen": (120, 180), "estado": "ACTIVO", "antiguedad": 2},

    {"nombre": "Panadería Trigo de Oro", "nit": "1090556781", "dv": "3",
     "actividad": "1081", "direccion": "Calle 3 # 8-15, barrio Aeropuerto",
     "telefono": "3143329871", "correo": "trigodeoro.cuc@gmail.com",
     "plan": "BASICO", "prefijo": "PTO", "resolucion": "18764003813877",
     "volumen": (40, 90), "estado": "ACTIVO", "antiguedad": 2},

    {"nombre": "Constructora Cúcuta Norte S.A.S.", "nit": "901208664", "dv": "5",
     "actividad": "4111", "direccion": "Av. Demetrio Mendoza # 4-90",
     "telefono": "6075830044", "correo": "contabilidad@ccnorte.com.co",
     "plan": "PRO", "prefijo": "CCN", "resolucion": "18764003813990",
     "volumen": (15, 40), "estado": "ACTIVO", "antiguedad": 1},
]

# Los compradores de nuestros clientes. No son clientes nuestros: son de ellos, y
# por eso viven en `receptores` y no en `customers`.
NOMBRES = ["Ana María Rodríguez", "Carlos Andrés Peña", "Luisa Fernanda Ortiz",
           "Jorge Enrique Salazar", "Diana Carolina Mejía", "Óscar Iván Torres",
           "Paula Andrea Jaimes", "Néstor Fabián Quintero", "Sandra Milena Rincón",
           "Julián David Cárdenas", "Marcela Vanegas", "Héctor Manuel Bautista",
           "Yeimy Katherine Suárez", "Andrés Felipe Contreras", "Rosa Elvira Parra"]

EMPRESAS_COMPRADORAS = [
    ("Inversiones El Portal S.A.S.", "900775231"),
    ("Comercializadora Andina Ltda.", "901003874"),
    ("Servicios Integrales del Oriente", "900412669"),
]

# El porcentaje del descuento no dice de dónde salió; el concepto sí, y es lo que
# la DIAN espera en el AllowanceChargeReason de la línea. Va atado al porcentaje
# para que el sembrador siga siendo determinista.
CONCEPTOS_DESCUENTO = {
    5: "Descuento comercial",
    10: "Promoción por volumen",
}

CONCEPTOS = {
    "4741": [("Portátil Lenovo IdeaPad 3", 2150000), ("Impresora Epson L3250", 890000),
             ("Teclado mecánico", 189000), ("Mouse inalámbrico", 45000),
             ("Memoria USB 64 GB", 38000)],
    "4772": [("Acetaminofén 500 mg x20", 8500), ("Suero fisiológico 500 ml", 12000),
             ("Alcohol antiséptico 700 ml", 9800), ("Vitamina C 1 g x10", 15600),
             ("Termómetro digital", 32000)],
    "4752": [("Cemento gris 50 kg", 34500), ("Pintura vinilo tipo 1 galón", 78000),
             ("Tubo PVC 1/2\" x 6 m", 14200), ("Juego de brocas 13 pzas", 42000),
             ("Cerradura de seguridad", 96000)],
    "4921": [("Flete Cúcuta – Bucaramanga", 320000), ("Flete Cúcuta – Bogotá", 780000),
             ("Encomienda urbana", 28000), ("Servicio de mudanza", 950000)],
    "4761": [("Resma papel carta", 21500), ("Cuaderno cosido 100 hojas", 6800),
             ("Caja de lapiceros x12", 18400), ("Cartulina pliego", 1800)],
    "5611": [("Almuerzo ejecutivo", 18000), ("Bandeja paisa", 32000),
             ("Jugo natural", 6000), ("Servicio de catering", 850000)],
    "4631": [("Leche entera caja x12", 48000), ("Queso doble crema kg", 22000),
             ("Yogur garrafa 2 L", 14500), ("Mantequilla 250 g", 8900)],
    "4520": [("Cambio de aceite y filtro", 145000), ("Alineación y balanceo", 90000),
             ("Pastillas de freno", 210000), ("Revisión general", 75000)],
    "1410": [("Uniforme escolar completo", 135000), ("Dotación empresarial x3", 420000),
             ("Camisa a la medida", 68000), ("Arreglo de prenda", 15000)],
    "4711": [("Mercado familiar", 185000), ("Arroz 5 kg", 24500),
             ("Aceite girasol 3 L", 38000), ("Carne de res kg", 32000)],
    "8622": [("Consulta y valoración", 60000), ("Limpieza dental", 130000),
             ("Resina en diente", 180000), ("Ortodoncia, cuota mensual", 250000)],
    "5511": [("Habitación sencilla, noche", 180000), ("Habitación doble, noche", 260000),
             ("Salón de eventos, día", 950000), ("Desayuno adicional", 22000)],
    "1081": [("Pan de queso x12", 12000), ("Torta de cumpleaños", 85000),
             ("Ponqué porción", 4500), ("Pedido para evento", 320000)],
    "4111": [("Anticipo de obra", 12500000), ("Acta parcial de obra", 8400000),
             ("Estudio de suelos", 2800000), ("Diseño arquitectónico", 4500000)],
}


class Manifiesto:
    """Todo lo creado, para poder deshacerlo sin adivinar."""

    def __init__(self):
        self.datos = {"generado": None, "empresa_factugest": None, "empresas": [],
                      "clientes": [], "productos": [], "clientes_api": [],
                      "receptores": [], "documentos": [], "facturas": [],
                      "consecutivos_previos": {}, "empresa_previa_usuarios": {},
                      "clientes_api_previos": {}}

    def guardar(self):
        self.datos["generado"] = datetime.now().isoformat(timespec="seconds")
        with open(MANIFIESTO, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, indent=2, ensure_ascii=False)

    @staticmethod
    def cargar():
        if not os.path.exists(MANIFIESTO):
            return None
        with open(MANIFIESTO, encoding="utf-8") as f:
            m = Manifiesto()
            m.datos = json.load(f)
            return m


# ── Utilidades ───────────────────────────────────────────────────────────────

def _primero_de_mes(referencia: date, atras: int = 0) -> date:
    """El primer día del mes, contando `atras` meses hacia el pasado."""
    mes = referencia.month - atras
    anio = referencia.year
    while mes <= 0:
        mes += 12
        anio -= 1
    return date(anio, mes, 1)


def _fin_de_mes(dia: date) -> date:
    return _primero_de_mes(dia, atras=-1) - timedelta(days=1)


def _periodo(dia: date) -> str:
    return f"{dia.year:04d}-{dia.month:02d}"


def _guardar_consecutivos(manifiesto, cod_empresa: int):
    """Los consecutivos previos, para que --limpiar no los deje adelantados."""
    clave = str(cod_empresa)
    if clave in manifiesto.datos["consecutivos_previos"]:
        return
    fila = get_one("SELECT consecutivo_actual, consecutivo_nc, consecutivo_nd "
                   "FROM empresas WHERE cod_empresa = %s", (cod_empresa,))
    if fila:
        manifiesto.datos["consecutivos_previos"][clave] = {
            k: int(v or 1) for k, v in fila.items()}


# ── Siembra ──────────────────────────────────────────────────────────────────

def sembrar_emisor(manifiesto) -> int:
    """La empresa con la que facturamos nosotros."""
    existente = get_one("SELECT cod_empresa FROM empresas WHERE nit = %s",
                        (EMISOR["nit"],))
    if existente:
        return existente["cod_empresa"]

    with transaction() as cur:
        cur.execute(
            "INSERT INTO empresas (nombre, nit, dv, direccion, ciudad, telefono, correo, "
            "  website, regimen_tributario, actividad_economica, tipo_documento, "
            "  cod_municipio, prefijo_factura, resolucion_dian, resolucion_fecha_desde, "
            "  resolucion_fecha_hasta, resolucion_desde, resolucion_hasta, "
            "  consecutivo_actual, consecutivo_nc, consecutivo_nd) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1,1,1)",
            (EMISOR["nombre"], EMISOR["nit"], EMISOR["dv"], EMISOR["direccion"],
             EMISOR["ciudad"], EMISOR["telefono"], EMISOR["correo"], EMISOR["website"],
             EMISOR["regimen_tributario"], EMISOR["actividad_economica"],
             EMISOR["tipo_documento"], EMISOR["cod_municipio"], EMISOR["prefijo_factura"],
             EMISOR["resolucion_dian"], f"{HOY.year}-01-01", f"{HOY.year}-12-31",
             EMISOR["resolucion_desde"], EMISOR["resolucion_hasta"]))
        cod = cur.lastrowid

    manifiesto.datos["empresa_factugest"] = cod
    _poner_logo(cod)
    return cod


def _poner_logo(cod_empresa: int):
    """Deja cargado nuestro logo para el membrete de nuestras facturas.

    Los suscriptores quedan sin logo a propósito: es el estado normal de un
    cliente recién integrado, y sirve para ver que el membrete imprime bien su
    nombre cuando no hay imagen. Se les carga desde Empresas emisoras › Logo.
    """
    from services.avatar_service import FotoInvalidaError, guardar_logo
    origen = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "static", "img", "logodark2.png")
    if not os.path.exists(origen):
        return
    try:
        with open(origen, "rb") as f:
            nombre = guardar_logo(f.read(), cod_empresa)
        execute_update(
            "UPDATE empresas SET logo = %s, color_marca = %s WHERE cod_empresa = %s",
            (nombre, "#4e73df", cod_empresa))
    except (FotoInvalidaError, OSError):
        pass


def mudar_usuarios(manifiesto, cod_empresa: int):
    """Los usuarios del panel pasan a ser empleados de FactuGest.

    El tablero filtra por la empresa del usuario. Mientras nuestro administrador
    siga registrado en la tienda de `seed_demo`, al entrar verá las ventas de esa
    tienda y no las suscripciones, que es justo lo que esta fase corrige.
    """
    usuarios = get_many("SELECT cod_usuario, cod_empresa FROM usuarios "
                        "WHERE correo LIKE %s", ("%@factugest.com",))
    for u in usuarios:
        if u["cod_empresa"] == cod_empresa:
            continue
        manifiesto.datos["empresa_previa_usuarios"][str(u["cod_usuario"])] = u["cod_empresa"]
        execute_update("UPDATE usuarios SET cod_empresa = %s WHERE cod_usuario = %s",
                       (cod_empresa, u["cod_usuario"]))
    return len(manifiesto.datos["empresa_previa_usuarios"])


def sembrar_planes(manifiesto) -> dict:
    """Los planes son productos de servicio: se venden, pero no se descuentan de un stock."""
    por_sku = {}
    with transaction() as cur:
        for sku, nombre, descripcion, precio, unidad in PRODUCTOS:
            cur.execute("SELECT cod_producto FROM productos WHERE sku = %s", (sku,))
            fila = cur.fetchall()
            if fila:
                por_sku[sku] = fila[0]["cod_producto"]
                continue
            cur.execute(
                "INSERT INTO productos (sku, nombre, descripcion, precio_unitario, stock, "
                "  stock_minimo, controla_stock, cod_impuesto, unidad_medida, activo, tipo_item) "
                "VALUES (%s, %s, %s, %s, 0, 0, 0, %s, %s, 1, 'SV')",
                (sku, nombre, descripcion, precio, IVA, unidad))
            por_sku[sku] = cur.lastrowid
            manifiesto.datos["productos"].append(cur.lastrowid)
    return por_sku


def sembrar_suscriptores(manifiesto) -> list:
    """Cada suscriptor son tres filas: a quién le cobramos, con qué emite y con qué llave."""
    suscriptores = []

    for datos in SUSCRIPTORES:
        nombre, nit, dv = datos["nombre"], datos["nit"], datos["dv"]
        actividad, direccion = datos["actividad"], datos["direccion"]
        telefono, correo = datos["telefono"], datos["correo"]
        plan, prefijo = datos["plan"], datos["prefijo"]
        resolucion, volumen, estado = datos["resolucion"], datos["volumen"], datos["estado"]

        empresa = get_one("SELECT cod_empresa FROM empresas WHERE nit = %s", (nit,))
        if empresa:
            cod_empresa = empresa["cod_empresa"]
        else:
            cod_empresa = _crear_empresa_cliente(nombre, nit, dv, actividad, direccion,
                                                 telefono, correo, prefijo, resolucion)
            manifiesto.datos["empresas"].append(cod_empresa)
        _guardar_consecutivos(manifiesto, cod_empresa)

        cliente = get_one("SELECT customer_id FROM customers WHERE document_number = %s",
                          (nit,))
        if cliente:
            cod_cliente = cliente["customer_id"]
        else:
            cod_cliente = _crear_customer(nombre, nit, telefono, correo, direccion)
            manifiesto.datos["clientes"].append(cod_cliente)

        cupo = PLANES[plan]["cupo"]
        api = get_one("SELECT cod_cliente_api, cod_cliente, plan, limite_mensual, estado "
                      "FROM clientes_api WHERE cod_empresa = %s", (cod_empresa,))
        if api:
            # La llave que ya existe se respeta: está en el .env del cliente y
            # rotarla aquí dejaría a Siste Soluciones sin poder emitir.
            manifiesto.datos["clientes_api_previos"][str(api["cod_cliente_api"])] = {
                "cod_cliente": api["cod_cliente"], "plan": api["plan"],
                "limite_mensual": api["limite_mensual"], "estado": api["estado"]}
            execute_update(
                "UPDATE clientes_api SET cod_cliente=%s, plan=%s, limite_mensual=%s, "
                "estado=%s WHERE cod_cliente_api=%s",
                (cod_cliente, plan, cupo, estado, api["cod_cliente_api"]))
            cod_api = api["cod_cliente_api"]
            llave = None
        else:
            cod_api, llave = crear_cliente_api(nombre, cod_empresa, cod_cliente, plan, cupo)
            if estado != "ACTIVO":
                execute_update("UPDATE clientes_api SET estado = %s WHERE cod_cliente_api = %s",
                               (estado, cod_api))
            manifiesto.datos["clientes_api"].append(cod_api)

        suscriptores.append({
            "cod_cliente_api": cod_api, "cod_empresa": cod_empresa,
            "cod_cliente": cod_cliente, "nombre": nombre, "plan": plan,
            "actividad": actividad, "volumen": volumen, "estado": estado,
            "llave": llave, "prefijo": prefijo,
            "antiguedad": datos["antiguedad"],
        })

    return suscriptores


def _crear_empresa_cliente(nombre, nit, dv, actividad, direccion, telefono, correo,
                           prefijo, resolucion) -> int:
    with transaction() as cur:
        cur.execute(
            "INSERT INTO empresas (nombre, nit, dv, direccion, ciudad, telefono, correo, "
            "  regimen_tributario, actividad_economica, tipo_documento, cod_municipio, "
            "  prefijo_factura, resolucion_dian, resolucion_fecha_desde, "
            "  resolucion_fecha_hasta, resolucion_desde, resolucion_hasta, "
            "  consecutivo_actual, consecutivo_nc, consecutivo_nd) "
            "VALUES (%s,%s,%s,%s,'San Jose De Cucuta',%s,%s,'RESPONSABLE_IVA',%s,'NIT',"
            "        '54001',%s,%s,%s,%s,1,20000,1,1,1)",
            (nombre, nit, dv, direccion, telefono, correo, actividad, prefijo,
             resolucion, f"{HOY.year}-01-01", f"{HOY.year}-12-31"))
        return cur.lastrowid


def _crear_customer(nombre, nit, telefono, correo, direccion) -> int:
    with transaction() as cur:
        cur.execute(
            "INSERT INTO customers (full_name, document_type, document_number, phone, "
            "  email, address, ciudad, departamento, pais, tipo_persona, "
            "  regimen_tributario, cod_municipio, activo) "
            "VALUES (%s, '31', %s, %s, %s, %s, 'San José de Cúcuta', "
            "        'Norte de Santander', 'Colombia', 'JURIDICA', 'RESPONSABLE_IVA', "
            "        '54001', 1)",
            (nombre, nit, telefono, correo, direccion))
        return cur.lastrowid


def sembrar_receptores(manifiesto, suscriptores) -> dict:
    """El padrón de compradores de cada cliente. Se reutiliza entre documentos."""
    por_cliente = {}
    with transaction() as cur:
        for s in suscriptores:
            receptores = []
            for i, nombre in enumerate(NOMBRES):
                documento = str(1090100000 + s["cod_cliente_api"] * 977 + i * 13)
                cur.execute(
                    "SELECT cod_receptor FROM receptores WHERE cod_cliente_api = %s "
                    "AND tipo_documento = '13' AND numero_documento = %s",
                    (s["cod_cliente_api"], documento))
                fila = cur.fetchall()
                if fila:
                    receptores.append(fila[0]["cod_receptor"])
                    continue
                cur.execute(
                    "INSERT INTO receptores (cod_cliente_api, tipo_documento, "
                    "  numero_documento, nombre, tipo_persona, regimen_tributario, "
                    "  email, telefono, direccion, cod_municipio, creado_en) "
                    "VALUES (%s, '13', %s, %s, 'NATURAL', 'NO_RESPONSABLE_IVA', %s, %s, "
                    "        %s, '54001', %s)",
                    (s["cod_cliente_api"], documento, nombre,
                     nombre.split()[0].lower() + "@correo.com",
                     f"31{random.randint(10000000, 99999999)}",
                     f"Calle {random.randint(1, 30)} # {random.randint(1, 20)}-"
                     f"{random.randint(10, 99)}",
                     datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                receptores.append(cur.lastrowid)
                manifiesto.datos["receptores"].append(cur.lastrowid)

            for j, (razon, nit_comprador) in enumerate(EMPRESAS_COMPRADORAS):
                documento = f"{int(nit_comprador) + s['cod_cliente_api']}"
                cur.execute(
                    "SELECT cod_receptor FROM receptores WHERE cod_cliente_api = %s "
                    "AND tipo_documento = '31' AND numero_documento = %s",
                    (s["cod_cliente_api"], documento))
                fila = cur.fetchall()
                if fila:
                    receptores.append(fila[0]["cod_receptor"])
                    continue
                cur.execute(
                    "INSERT INTO receptores (cod_cliente_api, tipo_documento, "
                    "  numero_documento, dv, nombre, tipo_persona, regimen_tributario, "
                    "  email, telefono, direccion, cod_municipio, creado_en) "
                    "VALUES (%s, '31', %s, %s, %s, 'JURIDICA', 'RESPONSABLE_IVA', %s, %s, "
                    "        %s, '54001', %s)",
                    (s["cod_cliente_api"], documento, str(j + 2), razon,
                     "facturacion@" + razon.split()[0].lower() + ".com",
                     f"607{random.randint(5000000, 5999999)}",
                     f"Av. {random.randint(0, 9)} # {random.randint(1, 25)}-"
                     f"{random.randint(10, 99)}",
                     datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                receptores.append(cur.lastrowid)
                manifiesto.datos["receptores"].append(cur.lastrowid)

            por_cliente[s["cod_cliente_api"]] = receptores
    return por_cliente


def sembrar_trafico(manifiesto, suscriptores, receptores) -> int:
    """Los documentos que hemos emitido por cuenta de cada cliente.

    El consecutivo se lleva en memoria y se escribe una sola vez al final: son
    miles de documentos y hacerlo fila por fila con `reservar_numero` convertiría
    la siembra en un ejercicio de paciencia. La reserva atómica es para la
    emisión concurrente de verdad, no para un generador de un solo hilo.

    Eso sí, hay que respetar su misma convención: `consecutivo_actual` es **el
    siguiente número sin usar**, no el último usado. Guardarlo corrido en uno deja
    la base servida para que la primera emisión de verdad choque contra el índice
    único del emisor.
    """
    emitidos = 0
    empresas_creadas = get_many(
        "SELECT cod_empresa, nombre, nit, dv, prefijo_factura, resolucion_dian, "
        "       regimen_tributario, direccion, ciudad, telefono, correo, cod_municipio, "
        "       actividad_economica, resolucion_fecha_desde, resolucion_fecha_hasta, "
        "       resolucion_desde, resolucion_hasta "
        "FROM empresas")
    por_cod = {e["cod_empresa"]: e for e in empresas_creadas}

    for s in suscriptores:
        empresa = por_cod[s["cod_empresa"]]
        consecutivo = int(get_one("SELECT consecutivo_actual AS n FROM empresas "
                                  "WHERE cod_empresa = %s", (s["cod_empresa"],))["n"] or 1)
        conceptos = CONCEPTOS[s["actividad"]]
        pool = receptores[s["cod_cliente_api"]]

        with transaction() as cur:
            for atras in range(MESES_DE_TRAFICO - 1, -1, -1):
                # Nadie emite antes de contratarnos: el que lleva un mes con
                # nosotros no puede tener tres meses de documentos emitidos.
                if atras > s["antiguedad"]:
                    continue

                inicio = _primero_de_mes(HOY, atras)
                fin = min(_fin_de_mes(inicio), HOY)
                dias = (fin - inicio).days + 1

                cantidad = random.randint(*s["volumen"])
                if atras == 0:
                    # El mes en curso va a mitad de camino: el consumo del panel
                    # tiene que verse creciendo, no cerrado.
                    cantidad = int(cantidad * dias / 30)
                if s["estado"] != "ACTIVO" and atras == 0:
                    continue          # suspendido: dejó de emitir este mes

                for _ in range(cantidad):
                    dia = inicio + timedelta(days=random.randint(0, dias - 1))
                    cuando = datetime(dia.year, dia.month, dia.day,
                                      random.randint(8, 19), random.randint(0, 59),
                                      random.randint(0, 59))
                    _insertar_documento(cur, s, empresa, consecutivo, cuando,
                                        random.choice(pool), conceptos, manifiesto)
                    consecutivo += 1
                    emitidos += 1

            cur.execute("UPDATE empresas SET consecutivo_actual = %s WHERE cod_empresa = %s",
                        (consecutivo, s["cod_empresa"]))

    return emitidos


def _insertar_documento(cur, suscriptor, empresa, consecutivo, cuando, cod_receptor,
                        conceptos, manifiesto):
    lineas = []
    for descripcion, precio in random.sample(conceptos, random.randint(1, min(3, len(conceptos)))):
        desc_pct = random.choice([0, 0, 0, 5, 10])
        lineas.append({
            "codigo": descripcion[:12].upper().replace(" ", "-"),
            "descripcion": descripcion,
            "cantidad": random.randint(1, 4),
            "precio_unitario": precio,
            "descuento_porcentaje": desc_pct,
            "descripcion_descuento": CONCEPTOS_DESCUENTO.get(desc_pct),
            "impuesto_porcentaje": 19,
            "impuesto_codigo_dian": "01",
            "unidad_medida": "94",
        })
    calculo = calcular_documento(lineas)

    numero = f"{empresa['prefijo_factura']}{consecutivo}"
    cufe = generate_cufe({
        "numero_factura": numero, "fecha": cuando,
        "subtotal": calculo["subtotal"], "total_impuestos": calculo["total_impuestos"],
        "total": calculo["total"], "document_number": str(cod_receptor),
    }, empresa)

    # Casi todo se acepta; un puñado se rechaza para que el filtro por estado del
    # panel no sea decorativo y se vea qué hace un documento que no pasó.
    sorteo = random.random()
    estado = "ACEPTADO" if sorteo < 0.97 else ("RECHAZADO" if sorteo < 0.99 else "PENDIENTE")

    cur.execute(
        "INSERT INTO documentos (id_publico, cod_cliente_api, cod_empresa, cod_receptor, "
        "  tipo, prefijo, consecutivo, numero, cufe, qr, fecha_emision, forma_pago, "
        "  subtotal_bruto, total_descuentos, subtotal, total_impuestos, total, estado, "
        "  referencia_externa, proveedor_dian, creado_en) "
        "VALUES (%s,%s,%s,%s,'FV',%s,%s,%s,%s,%s,%s,'CONTADO',%s,%s,%s,%s,%s,%s,%s,"
        "        'simulado',%s)",
        ("doc_" + f"{suscriptor['cod_cliente_api']:02d}{consecutivo:08d}"[:12],
         suscriptor["cod_cliente_api"], suscriptor["cod_empresa"], cod_receptor,
         empresa["prefijo_factura"], consecutivo, numero, cufe,
         f"https://catalogo-vpfe.dian.gov.co/document/searchqr?documentkey={cufe}",
         cuando.strftime("%Y-%m-%d %H:%M:%S.%f"),
         calculo["subtotal_bruto"], calculo["total_descuentos"], calculo["subtotal"],
         calculo["total_impuestos"], calculo["total"], estado,
         f"VENTA-{suscriptor['cod_cliente_api']}-{consecutivo}",
         cuando.strftime("%Y-%m-%d %H:%M:%S")))
    cod_documento = cur.lastrowid
    manifiesto.datos["documentos"].append(cod_documento)

    for orden, linea in enumerate(calculo["lineas"], start=1):
        cur.execute(
            "INSERT INTO documento_lineas (cod_documento, orden, codigo, descripcion, "
            "  unidad_medida, cantidad, precio_unitario, valor_bruto, descuento_porcentaje, "
            "  descuento_valor, descripcion_descuento, subtotal, impuesto_codigo_dian, "
            "  impuesto_porcentaje, impuesto_valor) "
            "VALUES (%s,%s,%s,%s,'94',%s,%s,%s,%s,%s,%s,%s,'01',%s,%s)",
            (cod_documento, orden, linea["codigo"], linea["descripcion"],
             linea["cantidad"], linea["precio_unitario"], linea["valor_bruto"],
             linea["descuento_porcentaje"], linea["descuento_valor"],
             linea.get("descripcion_descuento"), linea["subtotal"],
             linea["impuesto_porcentaje"], linea["impuesto_valor"]))

    mensajes = {"ACEPTADO": "Documento validado por la DIAN",
                "RECHAZADO": "Rechazado: el receptor no está registrado en el RUT",
                "PENDIENTE": "En proceso de validación"}
    cur.execute(
        "INSERT INTO documento_eventos (cod_documento, tipo, proveedor, codigo, mensaje, "
        "  fecha) VALUES (%s, %s, 'simulado', %s, %s, %s)",
        (cod_documento, estado, "00" if estado == "ACEPTADO" else "89",
         mensajes[estado], cuando.strftime("%Y-%m-%d %H:%M:%S.%f")))


def _facturar(cur, manifiesto, empresa, cod_usuario, cod_cliente, lineas, emision,
              observaciones, estado_pago, plazo_dias, consecutivo) -> tuple:
    """Guarda una venta nuestra y devuelve (cod_factura, siguiente consecutivo).

    La usan las dos cosas que le vendemos a un cliente: la mensualidad del plan y
    los servicios que se cobran una sola vez al engancharlo.
    """
    calculo = calcular_documento(lineas)
    vencimiento = emision + timedelta(days=plazo_dias) if plazo_dias else None
    numero = f"{empresa['prefijo_factura']}{consecutivo}"

    cufe = generate_cufe({
        "numero_factura": numero, "fecha": emision,
        "subtotal": calculo["subtotal"], "total_impuestos": calculo["total_impuestos"],
        "total": calculo["total"], "document_number": str(cod_cliente),
    }, empresa)

    cur.execute(
        "INSERT INTO facturas (fecha, fecha_vencimiento, cod_cliente, cod_usuario, "
        "  cod_empresa, cod_metodo_pago, cod_pago, total, subtotal, total_descuentos, "
        "  total_impuestos, tipo_factura, observaciones, cufe, numero_factura, forma_pago) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'FV',%s,%s,%s,%s)",
        (emision.strftime("%Y-%m-%d 09:00:00"),
         vencimiento.strftime("%Y-%m-%d") if vencimiento else None,
         cod_cliente, cod_usuario, empresa["cod_empresa"], TRANSFERENCIA, estado_pago,
         calculo["total"], calculo["subtotal"], calculo["total_descuentos"],
         calculo["total_impuestos"], observaciones, cufe, numero,
         "CREDITO" if plazo_dias else "CONTADO"))
    cod_factura = cur.lastrowid
    manifiesto.datos["facturas"].append(cod_factura)

    for linea in calculo["lineas"]:
        cur.execute(
            "INSERT INTO detalle_factura (cod_factura, cod_producto, descripcion, "
            "  cantidad, precio_unitario, subtotal, descuento_porcentaje, "
            "  descuento_valor, impuesto_porcentaje, impuesto_valor) "
            "VALUES (%s,%s,%s,%s,%s,%s,0,0,%s,%s)",
            (cod_factura, linea["cod_producto"], linea["descripcion"],
             linea["cantidad"], linea["precio_unitario"], linea["subtotal"],
             linea["impuesto_porcentaje"], linea["impuesto_valor"]))

    return cod_factura, consecutivo + 1


def sembrar_mensualidades(manifiesto, suscriptores, productos, cod_empresa) -> int:
    """Lo que le vendemos a cada cliente: el enganche y la mensualidad.

    El mes en curso no se cobra: queda para el módulo de facturación de planes,
    que es el que emite llamando a nuestra propia API.
    """
    cod_usuario = (get_one("SELECT cod_usuario FROM usuarios WHERE rol = 'ADMIN' "
                           "ORDER BY cod_usuario LIMIT 1") or {}).get("cod_usuario", 1)
    consecutivo = int(get_one("SELECT consecutivo_actual AS n FROM empresas "
                              "WHERE cod_empresa = %s", (cod_empresa,))["n"] or 1)
    _guardar_consecutivos(manifiesto, cod_empresa)
    empresa = get_one("SELECT * FROM empresas WHERE cod_empresa = %s", (cod_empresa,))
    emitidas = 0

    with transaction() as cur:
        # El enganche: cuando un cliente entra se le cobra la implementación y, según
        # el caso, la habilitación ante la DIAN y la capacitación. Es lo que hace que
        # el mes en que entra un cliente nuevo se vea distinto en el tablero.
        for s in suscriptores:
            if s["antiguedad"] > MESES_DE_COBRO:
                continue
            servicios = ["IMPL-API"] + random.sample(
                [sku for sku in SERVICIOS_DE_ENGANCHE if sku != "IMPL-API"],
                random.randint(0, 2))
            lineas = []
            for sku in servicios:
                producto = next(p for p in PRODUCTOS if p[0] == sku)
                lineas.append({
                    "cod_producto": productos[sku], "descripcion": producto[1],
                    "cantidad": 1, "precio_unitario": producto[3],
                    "descuento_porcentaje": 0, "impuesto_porcentaje": 19,
                })

            alta = _primero_de_mes(HOY, s["antiguedad"]) + timedelta(days=2)
            cod_factura, consecutivo = _facturar(
                cur, manifiesto, empresa, cod_usuario, s["cod_cliente"], lineas, alta,
                f"Puesta en marcha de {s['nombre']}", PAGADA, 0, consecutivo)
            emitidas += 1

        # Se cobra hasta el antepenúltimo mes: el mes cerrado más reciente queda sin
        # cobrar a propósito. Es el que tiene el consumo completo —con los clientes
        # que se pasaron del cupo— y es el que se factura en vivo en la demostración.
        for atras in range(MESES_DE_COBRO, 1, -1):
            mes = _primero_de_mes(HOY, atras)
            for s in suscriptores:
                if atras > s["antiguedad"]:
                    continue          # todavía no era cliente
                if s["estado"] == "SUSPENDIDO" and atras <= 2:
                    continue          # dejó de pagar: por eso está suspendido

                plan = PLANES[s["plan"]]
                lineas = [{
                    "cod_producto": productos[plan["sku"]],
                    "descripcion": f"Suscripción {s['plan'].title()} — {_periodo(mes)}",
                    "cantidad": 1, "precio_unitario": plan["precio"],
                    "descuento_porcentaje": 0, "impuesto_porcentaje": 19,
                }]

                # Se cobra el día 5 del mes siguiente al consumido: primero se sabe
                # cuánto emitió, después se le pasa la cuenta.
                emision = _primero_de_mes(HOY, atras - 1) + timedelta(days=4)
                vencida = emision + timedelta(days=15) < HOY
                estado = PAGADA if atras >= 3 else (VENCIDA if vencida else PENDIENTE)

                cod_factura, consecutivo = _facturar(
                    cur, manifiesto, empresa, cod_usuario, s["cod_cliente"], lineas,
                    emision,
                    f"Suscripción {s['plan'].title()} del periodo {_periodo(mes)}",
                    estado, 15, consecutivo)
                emitidas += 1

                cur.execute(
                    "INSERT INTO facturas_plan (cod_cliente_api, periodo, cod_factura, "
                    "  documentos_emitidos, documentos_excedente, creado_en) "
                    "VALUES (%s, %s, %s, 0, 0, %s)",
                    (s["cod_cliente_api"], _periodo(mes), cod_factura,
                     datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        cur.execute("UPDATE empresas SET consecutivo_actual = %s WHERE cod_empresa = %s",
                    (consecutivo, cod_empresa))

        # El consumo que cada mensualidad cobró se congela al facturar: si mañana
        # se emite un documento con fecha vieja, la factura ya cerrada no cambia.
        cur.execute("""
            UPDATE facturas_plan fp
            SET fp.documentos_emitidos = (
                    SELECT COUNT(*) FROM documentos d
                    WHERE d.cod_cliente_api = fp.cod_cliente_api
                      AND DATE_FORMAT(d.fecha_emision, '%Y-%m') = fp.periodo)
        """)

    return emitidas


def sembrar_autoservicio(manifiesto, cod_empresa) -> str:
    """FactuGest como cliente de su propia API.

    Es lo que permite que la mensualidad de un cliente se emita por el mismo
    servicio que le vendemos, en vez de por un camino privilegiado que nadie más
    tiene. Si el producto no sirve para facturarnos a nosotros, no sirve.
    """
    cod_cliente = (get_one("SELECT customer_id FROM customers WHERE document_number = %s",
                           (EMISOR["nit"],)) or {}).get("customer_id")
    existente = get_one("SELECT cod_cliente_api FROM clientes_api WHERE cod_empresa = %s",
                        (cod_empresa,))
    if existente:
        return None

    cod, llave = crear_cliente_api("FactuGest — autoservicio", cod_empresa, cod_cliente,
                                   "ILIMITADO", None)
    manifiesto.datos["clientes_api"].append(cod)
    return llave


# ── Verificación ─────────────────────────────────────────────────────────────

def verificar(cod_empresa: int) -> list:
    problemas = []

    huerfanos = get_one(
        "SELECT COUNT(*) c FROM documentos d "
        "LEFT JOIN documento_lineas l ON d.cod_documento = l.cod_documento "
        "WHERE l.cod_linea IS NULL")["c"]
    if huerfanos:
        problemas.append(f"{huerfanos} documento(s) sin líneas")

    descuadre = get_one(
        "SELECT COUNT(*) c FROM ("
        "  SELECT d.cod_documento FROM documentos d "
        "  JOIN documento_lineas l ON d.cod_documento = l.cod_documento "
        "  GROUP BY d.cod_documento, d.total "
        "  HAVING ABS(d.total - SUM(l.subtotal + l.impuesto_valor)) > 0.05) x")["c"]
    if descuadre:
        problemas.append(f"{descuadre} documento(s) con total distinto a la suma de sus líneas")

    repetidos = get_one(
        "SELECT COUNT(*) c FROM ("
        "  SELECT cod_empresa, tipo, numero FROM documentos "
        "  GROUP BY cod_empresa, tipo, numero HAVING COUNT(*) > 1) x")["c"]
    if repetidos:
        problemas.append(f"{repetidos} número(s) de documento repetidos en un mismo emisor")

    # Que el contador quede por delante del último número usado. Si no, la
    # siguiente emisión de verdad reserva un número que ya está en la base.
    for e in get_many(
            "SELECT e.cod_empresa, e.nombre, e.consecutivo_actual, "
            "       MAX(d.consecutivo) AS ultimo "
            "FROM empresas e JOIN documentos d ON d.cod_empresa = e.cod_empresa "
            "GROUP BY e.cod_empresa"):
        if e["ultimo"] is not None and int(e["ultimo"]) >= int(e["consecutivo_actual"] or 1):
            problemas.append(
                f"{e['nombre']}: el consecutivo va en {e['consecutivo_actual']} pero ya "
                f"existe el documento {e['ultimo']}")

    # El autoservicio es la excepción legítima: no nos cobramos la suscripción a
    # nosotros mismos, así que no tiene fila en `customers`.
    sin_plan = get_one(
        "SELECT COUNT(*) c FROM clientes_api WHERE cod_cliente IS NULL "
        "AND cod_empresa <> %s", (cod_empresa,))["c"]
    if sin_plan:
        problemas.append(f"{sin_plan} cliente(s) API sin la fila de customers a la que se le cobra")

    facturas = get_one("SELECT COUNT(*) c FROM facturas WHERE cod_empresa = %s",
                       (cod_empresa,))["c"]
    if not facturas:
        problemas.append("FactuGest no tiene ninguna venta: el tablero saldría vacío")

    return problemas


def resumen(cod_empresa: int):
    print("\nResumen:")
    fila = get_one(
        "SELECT COUNT(*) c, COALESCE(SUM(total), 0) t FROM facturas WHERE cod_empresa = %s",
        (cod_empresa,))
    print(f"  Mensualidades facturadas   {fila['c']}  ·  ${fila['t']:,.0f}")

    for f in get_many(
            "SELECT ca.nombre, ca.plan, ca.limite_mensual, ca.estado, "
            "       COUNT(d.cod_documento) AS emitidos "
            "FROM clientes_api ca "
            "LEFT JOIN documentos d ON d.cod_cliente_api = ca.cod_cliente_api "
            "GROUP BY ca.cod_cliente_api ORDER BY emitidos DESC"):
        cupo = f["limite_mensual"] or "sin tope"
        print(f"  {f['nombre'][:34]:<34} {f['plan']:<10} cupo {str(cupo):<9} "
              f"{f['emitidos']:>5} documentos  [{f['estado']}]")


# ── Limpieza ─────────────────────────────────────────────────────────────────

def limpiar():
    m = Manifiesto.cargar()
    if not m:
        print("No hay manifiesto: no se sembró nada con este script o ya se limpió.")
        return
    d = m.datos

    for cod in d["facturas"]:
        execute_update("DELETE FROM facturas_plan WHERE cod_factura = %s", (cod,))
        execute_update("DELETE FROM detalle_factura WHERE cod_factura = %s", (cod,))
        execute_update("DELETE FROM facturas WHERE cod_factura = %s", (cod,))

    if d["documentos"]:
        marcas = ",".join(["%s"] * len(d["documentos"]))
        execute_update(f"DELETE FROM documentos WHERE cod_documento IN ({marcas})",
                       tuple(d["documentos"]))

    for cod in d["receptores"]:
        execute_update("DELETE FROM receptores WHERE cod_receptor = %s", (cod,))

    for cod, previo in d.get("clientes_api_previos", {}).items():
        execute_update(
            "UPDATE clientes_api SET cod_cliente=%s, plan=%s, limite_mensual=%s, "
            "estado=%s WHERE cod_cliente_api=%s",
            (previo["cod_cliente"], previo["plan"], previo["limite_mensual"],
             previo["estado"], int(cod)))
    for cod in d["clientes_api"]:
        # Lo que ese cliente emitió después de la siembra —una mensualidad probada
        # a mano, por ejemplo— no está en el manifiesto, pero se va con él: son
        # documentos de un cliente que deja de existir, no de uno ajeno.
        execute_update("DELETE FROM documentos WHERE cod_cliente_api = %s", (cod,))
        execute_update("DELETE FROM clientes_api WHERE cod_cliente_api = %s", (cod,))

    for cod in d["productos"]:
        execute_update("DELETE FROM detalle_factura WHERE cod_producto = %s", (cod,))
        execute_update("DELETE FROM productos WHERE cod_producto = %s", (cod,))
    for cod in d["clientes"]:
        execute_update("DELETE FROM customers WHERE customer_id = %s", (cod,))

    for cod_usuario, cod_empresa in d.get("empresa_previa_usuarios", {}).items():
        execute_update("UPDATE usuarios SET cod_empresa = %s WHERE cod_usuario = %s",
                       (cod_empresa, int(cod_usuario)))

    for cod_empresa, cons in d["consecutivos_previos"].items():
        execute_update(
            "UPDATE empresas SET consecutivo_actual=%s, consecutivo_nc=%s, "
            "consecutivo_nd=%s WHERE cod_empresa=%s",
            (cons["consecutivo_actual"], cons["consecutivo_nc"], cons["consecutivo_nd"],
             int(cod_empresa)))

    for cod in d["empresas"]:
        execute_update("DELETE FROM empresas WHERE cod_empresa = %s", (cod,))
    if d.get("empresa_factugest"):
        execute_update("DELETE FROM empresas WHERE cod_empresa = %s",
                       (d["empresa_factugest"],))

    os.remove(MANIFIESTO)
    print(f"Limpieza completa: {len(d['facturas'])} mensualidades, "
          f"{len(d['documentos'])} documentos, {len(d['clientes'])} clientes y "
          f"{len(d['empresas']) + 1} empresas eliminados; consecutivos restaurados.")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    parser = argparse.ArgumentParser(
        description="Datos de FactuGest como proveedor tecnológico")
    parser.add_argument("--limpiar", action="store_true",
                        help="deshace exactamente lo sembrado por este script")
    args = parser.parse_args()

    if args.limpiar:
        limpiar()
        return

    if os.path.exists(MANIFIESTO):
        print("Ya hay datos sembrados.\n"
              "Ejecuta primero:  python seed_proveedor.py --limpiar")
        sys.exit(1)

    random.seed(SEMILLA)
    print("Sembrando la operación de FactuGest como proveedor...")
    manifiesto = Manifiesto()
    try:
        cod_empresa = sembrar_emisor(manifiesto)
        print(f"  empresa emisora FactuGest S.A.S. (cod {cod_empresa})")

        mudados = mudar_usuarios(manifiesto, cod_empresa)
        if mudados:
            print(f"  {mudados} usuario(s) del panel pasaron a la empresa FactuGest")

        productos = sembrar_planes(manifiesto)
        print(f"  {len(productos)} planes y servicios en el catálogo")

        suscriptores = sembrar_suscriptores(manifiesto)
        print(f"  {len(suscriptores)} empresas suscritas")

        receptores = sembrar_receptores(manifiesto, suscriptores)
        print(f"  {sum(len(r) for r in receptores.values())} receptores en los padrones")

        documentos = sembrar_trafico(manifiesto, suscriptores, receptores)
        print(f"  {documentos} documentos emitidos por cuenta de terceros")

        mensualidades = sembrar_mensualidades(manifiesto, suscriptores, productos,
                                              cod_empresa)
        print(f"  {mensualidades} mensualidades facturadas")

        llave_propia = sembrar_autoservicio(manifiesto, cod_empresa)
    finally:
        manifiesto.guardar()

    problemas = verificar(cod_empresa)
    resumen(cod_empresa)

    nuevas = [(s["nombre"], s["llave"]) for s in suscriptores if s["llave"]]
    if nuevas or llave_propia:
        print("\n" + "=" * 74)
        print("LLAVES GENERADAS — se muestran una sola vez, guárdalas ahora")
        print("=" * 74)
        for nombre, llave in nuevas:
            print(f"  {nombre}\n    {llave}")
        if llave_propia:
            print("  FactuGest — autoservicio  (va en el .env de este mismo proyecto)")
            print(f"    FACTUGEST_API_KEY={llave_propia}")
        print("=" * 74)
        print("Si se pierde una, se rota desde el panel: Plataforma › Clientes API.")

    if problemas:
        print("\n[!] Inconsistencias detectadas:")
        for p in problemas:
            print("    -", p)
        sys.exit(1)
    print("\nVerificación: los documentos, sus líneas y las mensualidades cuadran.")


if __name__ == "__main__":
    main()
