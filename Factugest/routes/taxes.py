from fastapi import APIRouter, Request
from services.taxes import get_all_invoice_taxes
from templates_config import templates

router = APIRouter()


@router.get("/invoice_taxes", name="invoice_taxes")
def invoice_taxes(request: Request):
    data = get_all_invoice_taxes()
    return templates.TemplateResponse(request, "invoice_taxes/index.html", {"invoice_taxes": data})


@router.get("/taxes/new", name="taxes_new")
def taxes_new(request: Request):
    return templates.TemplateResponse(request, "invoice_taxes/form.html")
