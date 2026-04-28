from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from services.taxes import (get_all_invoice_taxes, get_tax_by_id,
                             create_tax, update_tax, delete_tax)
from templates_config import templates

router = APIRouter(prefix="/invoice_taxes")


@router.get("", name="invoice_taxes")
def invoice_taxes(request: Request):
    data = get_all_invoice_taxes()
    return templates.TemplateResponse(request, "invoice_taxes/index.html", {"all_taxes": data})


@router.get("/new", name="taxes_new")
def new_tax(request: Request):
    return templates.TemplateResponse(request, "invoice_taxes/form.html", {"tax": None})


@router.post("/new", name="create_tax")
def create_tax_post(
    descripcion: str = Form(...),
    porcentaje: float = Form(...),
    codigo_dian: str = Form(""),
):
    create_tax(descripcion, porcentaje, codigo_dian)
    return RedirectResponse(url="/invoice_taxes", status_code=303)


@router.get("/edit/{tax_id}", name="edit_tax")
def edit_tax(request: Request, tax_id: int):
    tax = get_tax_by_id(tax_id)
    if not tax:
        return RedirectResponse(url="/invoice_taxes", status_code=302)
    return templates.TemplateResponse(request, "invoice_taxes/form.html", {"tax": tax})


@router.post("/edit/{tax_id}", name="update_tax")
def update_tax_post(
    tax_id: int,
    descripcion: str = Form(...),
    porcentaje: float = Form(...),
    codigo_dian: str = Form(""),
):
    update_tax(tax_id, descripcion, porcentaje, codigo_dian)
    return RedirectResponse(url="/invoice_taxes", status_code=303)


@router.get("/delete/{tax_id}", name="delete_tax")
def delete_tax_get(tax_id: int):
    delete_tax(tax_id)
    return RedirectResponse(url="/invoice_taxes", status_code=302)
