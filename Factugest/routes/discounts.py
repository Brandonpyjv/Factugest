from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from services.discounts import (get_all_discount, get_discount_by_id,
                                 create_discount, update_discount, delete_discount)
from templates_config import templates

router = APIRouter(prefix="/discount")


@router.get("", name="discount")
def discount(request: Request):
    data = get_all_discount()
    return templates.TemplateResponse(request, "discount/index.html", {"all_discount": data})


@router.get("/new", name="new_discount")
def new_discount(request: Request):
    return templates.TemplateResponse(request, "discount/form.html", {"discount": None})


@router.post("/new", name="create_discount")
def create_discount_post(
    descripcion: str = Form(...),
    porcentaje: float = Form(...),
    aplica_a_producto: int = Form(0),
    aplica_a_factura: int = Form(0),
):
    create_discount(descripcion, porcentaje, aplica_a_producto, aplica_a_factura)
    return RedirectResponse(url="/discount", status_code=303)


@router.get("/edit/{discount_id}", name="edit_discount")
def edit_discount(request: Request, discount_id: int):
    d = get_discount_by_id(discount_id)
    if not d:
        return RedirectResponse(url="/discount", status_code=302)
    return templates.TemplateResponse(request, "discount/form.html", {"discount": d})


@router.post("/edit/{discount_id}", name="update_discount")
def update_discount_post(
    discount_id: int,
    descripcion: str = Form(...),
    porcentaje: float = Form(...),
    aplica_a_producto: int = Form(0),
    aplica_a_factura: int = Form(0),
):
    update_discount(discount_id, descripcion, porcentaje, aplica_a_producto, aplica_a_factura)
    return RedirectResponse(url="/discount", status_code=303)


@router.get("/delete/{discount_id}", name="delete_discount")
def delete_discount_get(discount_id: int):
    delete_discount(discount_id)
    return RedirectResponse(url="/discount", status_code=302)
