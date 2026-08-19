"""
Llaves de API de los clientes integrados.

Una llave se ve así:

    fg_live_7d3a9f21.mXk2Qp8vLr4TnW6yBc1ZsJd5HgF0aEuO

La parte antes del punto es el **prefijo**, que se guarda en claro y es lo único
que se muestra en el panel: sirve para identificar la llave sin revelarla y, sobre
todo, para encontrar la fila de un solo golpe. Sin él habría que traer todos los
clientes y comparar el hash contra cada uno en cada petición.

Lo que va después del punto es el **secreto**, que solo existe en el momento de
crearlo: de él se guarda el hash, nunca el valor. Si el cliente lo pierde, no se
recupera —se rota.

**Por qué SHA-256 y no bcrypt.** bcrypt es deliberadamente lento para que una
contraseña humana, con poca entropía, no se pueda romper por fuerza bruta. Un
secreto de 32 caracteres aleatorios no tiene ese problema: adivinarlo es
inviable por más rápido que sea el hash. Y esto corre en cada llamada a la API,
donde los ~100 ms de bcrypt sí se notarían. Las contraseñas de las personas
siguen con bcrypt en `auth.py`, que es donde hace falta.
"""
import hashlib
import hmac
import secrets
from datetime import datetime

from database import execute_query, execute_update, get_one, get_many
from services import validaciones as v

PREFIJO_BASE = "fg_live_"
ESTADOS = ("ACTIVO", "SUSPENDIDO", "REVOCADO")
PLANES = ("BASICO", "PRO", "ILIMITADO")

# Cupo con el que se propone cada plan. Es una sugerencia del formulario, no una
# regla: un cliente puede quedar con el cupo que se le haya negociado.
CUPO_SUGERIDO = {"BASICO": 150, "PRO": 400, "ILIMITADO": None}

ETIQUETA_ESTADO = {
    "ACTIVO":     ("Activo", "success"),
    "SUSPENDIDO": ("Suspendido", "warning"),
    "REVOCADO":   ("Revocado", "danger"),
}


class LlaveInvalidaError(Exception):
    """La llave no existe o el secreto no corresponde."""


class ClienteInactivoError(Exception):
    """La llave existe pero el cliente está suspendido o revocado."""

    def __init__(self, estado: str):
        self.estado = estado
        super().__init__(f"El cliente API está en estado {estado}")


def _hash(secreto: str) -> str:
    return hashlib.sha256(secreto.encode("utf-8")).hexdigest()


def generar_llave() -> tuple:
    """Devuelve (prefijo, llave_completa). El secreto no se guarda en ningún lado."""
    prefijo = PREFIJO_BASE + secrets.token_hex(4)
    secreto = secrets.token_urlsafe(24)
    return prefijo, f"{prefijo}.{secreto}"


def _partir(llave: str) -> tuple:
    """Separa prefijo y secreto. El prefijo lleva guiones bajos, por eso el punto."""
    llave = (llave or "").strip()
    if "." not in llave:
        raise LlaveInvalidaError("La llave no tiene el formato esperado")
    prefijo, _, secreto = llave.partition(".")
    if not prefijo or not secreto:
        raise LlaveInvalidaError("La llave no tiene el formato esperado")
    return prefijo, secreto


# ── Validación ──────────────────────────────────────────────────────────────

def validar_cliente_api(datos: dict, cod_cliente_api: int = None):
    """Reglas del alta de un cliente integrado.

    La empresa emisora es lo único que no puede faltar ni repetirse: es con su
    NIT y su resolución que se van a numerar los documentos, y dos clientes
    apuntando a la misma empresa se pisarían el consecutivo.
    """
    val = v.Validador()
    val.campo("nombre", v.razon_social, datos.get("nombre"), maximo=150)
    val.campo("cod_empresa", v.entero, datos.get("cod_empresa"), minimo=1)
    val.campo("plan", v.opcion, datos.get("plan"), PLANES)

    cliente = (datos.get("cod_cliente") or "").strip() if isinstance(
        datos.get("cod_cliente"), str) else datos.get("cod_cliente")
    if cliente in (None, "", "0"):
        val.datos["cod_cliente"] = None
    else:
        val.campo("cod_cliente", v.entero, cliente, minimo=1)

    # Sin límite es un valor legítimo —es lo que significa el plan ilimitado—, así
    # que el campo vacío no es un error: es NULL.
    limite = datos.get("limite_mensual")
    if limite in (None, "", "0"):
        val.datos["limite_mensual"] = None
    else:
        val.campo("limite_mensual", v.entero, limite, minimo=1, maximo=1000000)

    cod_empresa = val.datos.get("cod_empresa")
    if cod_empresa:
        ocupada = get_one(
            "SELECT cod_cliente_api, nombre FROM clientes_api WHERE cod_empresa = %s "
            "AND cod_cliente_api <> %s", (cod_empresa, cod_cliente_api or 0))
        if ocupada:
            val.errores["cod_empresa"] = (
                f"Esa empresa emisora ya es de «{ocupada['nombre']}». "
                "Cada cliente numera con la suya.")

    return val


def actualizar_cliente_api(cod_cliente_api: int, nombre: str, cod_empresa: int,
                           cod_cliente, plan: str, limite_mensual):
    """Cambia los datos comerciales. La llave no se toca aquí: se rota aparte."""
    return execute_update(
        "UPDATE clientes_api SET nombre = %s, cod_empresa = %s, cod_cliente = %s, "
        "  plan = %s, limite_mensual = %s WHERE cod_cliente_api = %s",
        (nombre, cod_empresa, cod_cliente, plan, limite_mensual, cod_cliente_api))


def tiene_documentos(cod_cliente_api: int) -> int:
    """Cuántos documentos emitió. Un cliente con documentos no se borra, se revoca."""
    fila = get_one("SELECT COUNT(*) AS n FROM documentos WHERE cod_cliente_api = %s",
                   (cod_cliente_api,))
    return int(fila["n"] if fila else 0)


def eliminar_cliente_api(cod_cliente_api: int):
    """Solo para el que nunca emitió nada.

    Los documentos son la prueba de lo que se transmitió a la DIAN por cuenta de
    ese cliente; borrarlos junto con su ficha dejaría emisiones sin dueño. Para
    cortarle el servicio a un cliente que sí operó está `REVOCADO`.
    """
    if tiene_documentos(cod_cliente_api):
        raise ValueError("Ese cliente ya emitió documentos: revócalo en lugar de borrarlo.")
    return execute_update("DELETE FROM clientes_api WHERE cod_cliente_api = %s",
                          (cod_cliente_api,))


# ── Alta y administración ───────────────────────────────────────────────────

def crear_cliente_api(nombre: str, cod_empresa: int, cod_cliente: int = None,
                      plan: str = "BASICO", limite_mensual: int = None) -> tuple:
    """Crea el cliente y devuelve (cod_cliente_api, llave_completa).

    La llave completa se devuelve una única vez, aquí. De ahí en adelante solo
    queda el prefijo, así que quien la crea tiene que entregarla en ese momento.
    """
    prefijo, llave = generar_llave()
    _, secreto = _partir(llave)
    cod = execute_query(
        "INSERT INTO clientes_api (nombre, cod_cliente, cod_empresa, api_key_prefijo, "
        "  api_key_hash, plan, limite_mensual, estado, creado_en) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, 'ACTIVO', %s)",
        (nombre, cod_cliente, cod_empresa, prefijo, _hash(secreto), plan, limite_mensual,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    return cod, llave


def rotar_llave(cod_cliente_api: int) -> str:
    """Reemplaza la llave y devuelve la nueva. La anterior deja de servir al instante."""
    prefijo, llave = generar_llave()
    _, secreto = _partir(llave)
    actualizadas = execute_update(
        "UPDATE clientes_api SET api_key_prefijo = %s, api_key_hash = %s "
        "WHERE cod_cliente_api = %s",
        (prefijo, _hash(secreto), cod_cliente_api),
    )
    if not actualizadas:
        raise ValueError(f"No existe el cliente API {cod_cliente_api}")
    return llave


def cambiar_estado(cod_cliente_api: int, estado: str):
    if estado not in ESTADOS:
        raise ValueError(f"Estado inválido: {estado}")
    return execute_update(
        "UPDATE clientes_api SET estado = %s WHERE cod_cliente_api = %s",
        (estado, cod_cliente_api),
    )


def get_cliente_api_by_id(cod_cliente_api: int):
    return get_one(
        "SELECT ca.*, e.nombre AS empresa_nombre, e.nit AS empresa_nit, "
        "       c.full_name AS cliente_nombre "
        "FROM clientes_api ca "
        "LEFT JOIN empresas e  ON ca.cod_empresa = e.cod_empresa "
        "LEFT JOIN customers c ON ca.cod_cliente = c.customer_id "
        "WHERE ca.cod_cliente_api = %s",
        (cod_cliente_api,),
    )


def get_all_clientes_api():
    """La lista del panel, con el volumen emitido al lado.

    El conteo va en la misma consulta y no en un bucle: son pocas filas, pero una
    consulta por cliente es el camino más corto a una lista que se arrastra
    cuando haya cincuenta.
    """
    return get_many(
        "SELECT ca.*, e.nombre AS empresa_nombre, e.nit AS empresa_nit, "
        "       c.full_name AS cliente_nombre, "
        "       COUNT(d.cod_documento) AS documentos_total, "
        "       COALESCE(SUM(LEFT(d.fecha_emision, 7) = LEFT(CURDATE(), 7)), 0) "
        "           AS documentos_mes "
        "FROM clientes_api ca "
        "LEFT JOIN empresas e   ON ca.cod_empresa = e.cod_empresa "
        "LEFT JOIN customers c  ON ca.cod_cliente = c.customer_id "
        "LEFT JOIN documentos d ON d.cod_cliente_api = ca.cod_cliente_api "
        "GROUP BY ca.cod_cliente_api "
        "ORDER BY ca.estado = 'REVOCADO', ca.nombre"
    )


# ── Autenticación ───────────────────────────────────────────────────────────

def autenticar(llave: str) -> dict:
    """Resuelve el cliente dueño de la llave.

    Lanza `LlaveInvalidaError` si no corresponde a nadie y `ClienteInactivoError`
    si el cliente está suspendido o revocado: son dos situaciones distintas y el
    que se integra necesita poder distinguirlas.
    """
    prefijo, secreto = _partir(llave)

    fila = get_one(
        "SELECT ca.*, e.nombre AS empresa_nombre, e.nit AS empresa_nit "
        "FROM clientes_api ca LEFT JOIN empresas e ON ca.cod_empresa = e.cod_empresa "
        "WHERE ca.api_key_prefijo = %s",
        (prefijo,),
    )
    if not fila:
        raise LlaveInvalidaError("La llave no corresponde a ningún cliente")

    # compare_digest y no ==: comparar cadena a cadena se detiene en el primer
    # carácter distinto, y ese tiempo delata cuánto se acertó del secreto.
    if not hmac.compare_digest(fila["api_key_hash"], _hash(secreto)):
        raise LlaveInvalidaError("La llave no corresponde a ningún cliente")

    if fila["estado"] != "ACTIVO":
        raise ClienteInactivoError(fila["estado"])

    execute_update(
        "UPDATE clientes_api SET ultimo_uso = %s WHERE cod_cliente_api = %s",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fila["cod_cliente_api"]),
    )
    return fila
