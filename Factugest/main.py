import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

load_dotenv()

from auth import AuthMiddleware, hash_password, role_label, puede_cambiar_foto
from templates_config import templates
from routes.login import router as login_router
from routes.invoice import router as invoice_router
from routes.users import router as users_router
from routes.customer import router as customer_router
from routes.payment_methods import router as payment_methods_router
from routes.discounts import router as discount_router
from routes.taxes import router as invoice_taxes_router
from routes.branches import router as branches_router
from routes.invoice_payments import router as invoice_payments_router
from routes.productos import router as products_router
from routes.inventory import router as inventory_router
from routes.auditoria import router as auditoria_router
from routes.ubicacion import router as ubicacion_router
from services.report_service import etiqueta_estado
from services.validaciones import (abreviatura_documento, nombre_documento,
                                   tipos_documento_ordenados)
from routes.dashboard import router as dashboard_router
from routes.reports import router as reports_router
from routes.perfil import router as perfil_router
from routes.clientes_api import router as clientes_api_router
from routes.documentos import router as documentos_router
from routes.consumo import router as consumo_router
from routes.configuracion import router as configuracion_router
from routes.api.v1.sistema import router as api_sistema_router
from routes.api.v1.facturas import router as api_facturas_router
from routes.api.v1.notas import router as api_notas_router
from routes.api.v1.errores import registrar_manejadores

DESCRIPCION_API = """
API de facturación electrónica para Colombia. Tu sistema envía los datos de una
venta y FactuGest se encarga del resto: calcula los impuestos, numera con **tu**
resolución de la DIAN, genera el CUFE, el XML UBL 2.1 y la representación gráfica
en PDF, transmite al proveedor tecnológico y te devuelve el documento validado.

No tienes que cambiar tu software: solo llamar a esta API.

### Cómo empezar

1. Pon tu llave en el encabezado `X-API-Key` de cada petición. Tiene la forma
   `fg_live_7d3a9f21.mXk2Qp8vLr4TnW6yBc1ZsJd5HgF0aEuO`.
2. Llama a `GET /api/v1/ping`. Si responde, la llave sirve y te dice con qué
   emisor vas a numerar. Es la prueba que conviene hacer antes de escribir nada.
3. Emite con `POST /api/v1/facturas`.

### Dos cosas que evitan los problemas típicos

**Manda siempre `referencia_externa`** con el identificador de la venta en tu
sistema. Si la red se cae y reintentas, el segundo intento devuelve la factura que
ya se emitió —con código `200` en lugar de `201`— en vez de emitir otra. Sin eso,
un reintento quema un segundo número de una resolución autorizada y finita.

**Los precios los pones tú, los impuestos los calculamos nosotros.** Envía la base
y la tarifa; el prorrateo del IVA sobre un descuento de factura, los redondeos y
los totales salen de aquí, iguales para todos los que se integran.

### Cuando algo sale mal

Todos los errores tienen la misma forma, del `401` al `500`:

```json
{"detail": {"codigo": "cupo_agotado", "mensaje": "...", "campo": null}}
```

Programa contra `codigo`, que es estable; `mensaje` está escrito para que lo lea
una persona y puede cambiar de redacción.
"""

ETIQUETAS_API = [
    {"name": "Sistema",
     "description": "Comprobar que la llave sirve. Lo primero que se prueba."},
    {"name": "Documentos",
     "description": "Emitir facturas y notas, consultarlas y descargar el PDF y el XML."},
]

app = FastAPI(
    title="FactuGest — API de facturación electrónica",
    description=DESCRIPCION_API,
    version="1.0",
    openapi_tags=ETIQUETAS_API,
    contact={"name": "FactuGest", "email": "integraciones@factugest.co"},
    license_info={"name": "Uso bajo contrato de servicio"},
)

# Los middlewares se ejecutan en orden inverso al registro:
# AuthMiddleware corre primero, luego SessionMiddleware lo prepara.
app.add_middleware(AuthMiddleware)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "factugest-dev-secret"))

app.mount("/static", StaticFiles(directory="static"), name="static")

# Las rutas de la web quedan fuera del esquema OpenAPI: son formularios HTML, no
# una API, y mezcladas con /api/v1 dejan la documentación de integración
# inservible para quien la va a leer.
app.include_router(login_router, include_in_schema=False)
app.include_router(users_router, include_in_schema=False)
app.include_router(customer_router, include_in_schema=False)
app.include_router(invoice_router, include_in_schema=False)
app.include_router(payment_methods_router, include_in_schema=False)
app.include_router(discount_router, include_in_schema=False)
app.include_router(invoice_taxes_router, include_in_schema=False)
app.include_router(branches_router, include_in_schema=False)
app.include_router(invoice_payments_router, include_in_schema=False)
app.include_router(products_router, include_in_schema=False)
app.include_router(inventory_router, include_in_schema=False)
app.include_router(auditoria_router, include_in_schema=False)
app.include_router(ubicacion_router, include_in_schema=False)
app.include_router(reports_router, include_in_schema=False)
app.include_router(perfil_router, include_in_schema=False)
app.include_router(dashboard_router, include_in_schema=False)

# Los tres módulos del proveedor: a quién le damos servicio, qué se emitió por
# cuenta de ellos y cuánto consumieron del plan que pagan.
app.include_router(clientes_api_router, include_in_schema=False)
app.include_router(documentos_router, include_in_schema=False)
app.include_router(consumo_router, include_in_schema=False)
app.include_router(configuracion_router, include_in_schema=False)

# API de integración: misma aplicación, otra puerta. Se autentica con la llave
# del cliente, no con la sesión de la web.
app.include_router(api_sistema_router)
app.include_router(api_facturas_router)
app.include_router(api_notas_router)

# Todos los errores de /api/ salen con la misma forma, incluidos los 422 de
# Pydantic y lo que nadie previó. Las rutas web siguen devolviendo HTML.
registrar_manejadores(app)

# Registrar url_for como global en Jinja2
templates.env.globals["url_for"] = app.url_path_for


def avatar_url(foto: str = None) -> str:
    """URL de la foto de perfil, o la silueta genérica si no tiene."""
    if foto:
        return app.url_path_for("static", path=f"img/perfiles/{foto}")
    return app.url_path_for("static", path="img/avatar-generico.svg")


def fecha_iso(valor) -> str:
    """Valor de un <input type="date">.

    Al volver de una validación fallida la fecha llega como el texto que envió el
    formulario; desde la base llega como date. El template no debería tener que
    saber cuál de las dos es.
    """
    if not valor:
        return ""
    if hasattr(valor, "strftime"):
        return valor.strftime("%Y-%m-%d")
    return str(valor)[:10]


templates.env.globals["avatar_url"] = avatar_url
templates.env.globals["fecha_iso"] = fecha_iso
templates.env.globals["role_label"] = role_label
templates.env.globals["puede_cambiar_foto"] = puede_cambiar_foto
templates.env.globals["etiqueta_estado"] = etiqueta_estado

# Los tipos de documento se guardan con el código de la DIAN; las vistas muestran
# la abreviatura, porque nadie lee «13» y entiende «cédula».
templates.env.globals["abreviatura_documento"] = abreviatura_documento
templates.env.globals["nombre_documento"] = nombre_documento
templates.env.globals["tipos_documento"] = tipos_documento_ordenados


@app.on_event("startup")
def migrate_passwords():
    """Hashea contraseñas en texto plano al arrancar (idempotente)."""
    from database import get_many, execute_update
    users = get_many("SELECT cod_usuario, contrasena FROM usuarios")
    for u in users:
        pwd = u.get("contrasena") or ""
        if pwd and not pwd.startswith("$2"):
            hashed = hash_password(pwd)
            execute_update(
                "UPDATE usuarios SET contrasena=%s WHERE cod_usuario=%s",
                (hashed, u["cod_usuario"]),
            )


# El navegador pide /favicon.ico en la raíz aunque los <link> apunten a /static.
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/img/favicon.ico", media_type="image/x-icon")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
