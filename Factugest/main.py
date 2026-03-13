from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from templates_config import templates
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

app = FastAPI(title="Factugest", description="Sistema de Facturación Electrónica Colombia")

app.mount("/static", StaticFiles(directory="static"), name="static")

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

# Registrar url_for como global en Jinja2 apuntando al router de la app
templates.env.globals["url_for"] = app.url_path_for


@app.get("/", name="index")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/settings", name="setting")
def setting(request: Request):
    return templates.TemplateResponse(request, "settings/index.html")


@app.get("/settings/new", name="settings_new")
def setting_new(request: Request):
    return templates.TemplateResponse(request, "settings/form.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
