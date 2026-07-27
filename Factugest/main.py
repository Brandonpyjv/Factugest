import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

load_dotenv()

from auth import AuthMiddleware, hash_password
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
from routes.logs import router as logs_router
from routes.product_discount import router as product_discount_router
from routes.ubicacion import router as ubicacion_router
from routes.api.v1.auth import router as api_v1_auth_router
from routes.api.v1.dashboard import router as api_v1_dashboard_router
from routes.api.v1.customers import router as api_v1_customers_router
from services.invoice_service import get_dashboard_stats

app = FastAPI(title="Factugest", description="Sistema de Facturación Electrónica Colombia")

# Los middlewares se ejecutan en orden inverso al registro:
# AuthMiddleware corre primero, luego SessionMiddleware lo prepara.
app.add_middleware(AuthMiddleware)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "factugest-dev-secret"))

# CORS: el cliente Flutter Web hace requests desde otro origen (localhost:xxxx aleatorio).
# Se agrega al final para que quede como capa más externa y atienda el preflight OPTIONS
# antes que AuthMiddleware redirija a /login.
# Para producción: reemplazar allow_origin_regex por una lista de dominios reales.
_cors_regex = os.getenv("CORS_ORIGIN_REGEX", r"https?://(localhost|127\.0\.0\.1)(:\d+)?")
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=_cors_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(login_router)
app.include_router(users_router)
app.include_router(customer_router)
app.include_router(invoice_router)
app.include_router(payment_methods_router)
app.include_router(discount_router)
app.include_router(invoice_taxes_router)
app.include_router(branches_router)
app.include_router(invoice_payments_router)
app.include_router(products_router)
app.include_router(logs_router)
app.include_router(product_discount_router)
app.include_router(ubicacion_router)

# ── API JSON para cliente móvil (autenticación vía JWT) ─────────────────────
app.include_router(api_v1_auth_router)
app.include_router(api_v1_dashboard_router)
app.include_router(api_v1_customers_router)

# Registrar url_for como global en Jinja2
templates.env.globals["url_for"] = app.url_path_for


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


@app.get("/", name="index")
def index(request: Request):
    stats = get_dashboard_stats()
    return templates.TemplateResponse(request, "index.html", {"stats": stats})


@app.get("/settings", name="setting")
def setting(request: Request):
    return templates.TemplateResponse(request, "settings/index.html")


@app.get("/settings/new", name="settings_new")
def setting_new(request: Request):
    return templates.TemplateResponse(request, "settings/form.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
