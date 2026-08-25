"""
FactuGest llamando a la API de FactuGest.

La mensualidad de un cliente se emite por la misma puerta que usa Siste
Soluciones: `POST /api/v1/facturas` con una llave en el encabezado. No hay atajo
interno ni función privilegiada, y eso es deliberado —si el producto no sirve
para facturarnos a nosotros, no sirve—. Cada vez que se cobra un plan se está
probando el servicio que se vende.

Es el mismo cliente HTTP que tiene el POS, con la misma tolerancia a fallos: si
la API no contesta, no se guarda nada y el botón se puede volver a pulsar. La
idempotencia por `referencia_externa` es lo que hace seguro reintentar.
"""
import os

import httpx

TIEMPO_LIMITE = 30.0


class AutoservicioError(Exception):
    """No se pudo emitir. `detalle` es lo que se le muestra a quien pulsó el botón."""

    def __init__(self, detalle: str, codigo: str = None):
        self.detalle = detalle
        self.codigo = codigo
        super().__init__(detalle)


def _url() -> str:
    return (os.getenv("FACTUGEST_URL") or "http://127.0.0.1:8000").rstrip("/")


def configurado() -> bool:
    """Para que la vista no ofrezca un botón que no puede funcionar."""
    return bool((os.getenv("FACTUGEST_API_KEY") or "").strip())


def _llave() -> str:
    llave = (os.getenv("FACTUGEST_API_KEY") or "").strip()
    if not llave:
        raise AutoservicioError(
            "Falta la llave de autoservicio. Créala en Plataforma › Clientes API, "
            "cópiala en FACTUGEST_API_KEY del archivo .env y reinicia el sistema.",
            codigo="sin_llave")
    return llave


def _pedir(metodo: str, ruta: str, **kwargs) -> httpx.Response:
    try:
        with httpx.Client(timeout=TIEMPO_LIMITE) as cliente:
            return cliente.request(metodo, _url() + ruta,
                                   headers={"X-API-Key": _llave()}, **kwargs)
    except httpx.TimeoutException:
        raise AutoservicioError(
            "La API no respondió a tiempo. No se guardó nada: vuelve a intentarlo.",
            codigo="timeout")
    except httpx.RequestError:
        raise AutoservicioError(
            f"No se pudo conectar con la API en {_url()}. Revisa que el servidor "
            "esté encendido y que FACTUGEST_URL apunte a él.", codigo="sin_conexion")


def _revisar(respuesta: httpx.Response) -> dict:
    if respuesta.status_code < 400:
        return respuesta.json()

    try:
        detalle = respuesta.json().get("detail")
    except Exception:
        detalle = None

    if isinstance(detalle, dict):
        codigo, mensaje = detalle.get("codigo"), detalle.get("mensaje")
    elif isinstance(detalle, list):
        codigo = "datos_invalidos"
        mensaje = "; ".join(
            f"{'.'.join(str(p) for p in e.get('loc', [])[1:])}: {e.get('msg')}"
            for e in detalle[:4])
    else:
        codigo, mensaje = "error", str(detalle or respuesta.text)[:300]

    raise AutoservicioError(mensaje or "La API rechazó el documento.", codigo=codigo)


def ping() -> dict:
    """Con qué emisor numera nuestra propia llave. También confirma que sirve."""
    return _revisar(_pedir("GET", "/api/v1/ping"))


def emitir(peticion: dict) -> dict:
    return _revisar(_pedir("POST", "/api/v1/facturas", json=peticion))
