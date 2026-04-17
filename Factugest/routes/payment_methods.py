from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from services.payment_methods_service import (get_all_payment_methods, get_payment_method_by_id,
                                               create_payment_method, update_payment_method, delete_payment_method)
from templates_config import templates

router = APIRouter(prefix="/payment_methods")


@router.get("", name="payment_methods")
def payment_methods(request: Request):
    data = get_all_payment_methods()
    return templates.TemplateResponse(request, "payment_methods/index.html", {"all_payment_methods": data})


@router.get("/new", name="payment_methods_new")
def new_payment_method(request: Request):
    return templates.TemplateResponse(request, "payment_methods/form.html", {"pm": None})


@router.post("/new", name="create_payment_method")
def create_payment_method_post(
    descripcion: str = Form(...),
    nombre: str = Form(""),
):
    create_payment_method(descripcion, nombre)
    return RedirectResponse(url="/payment_methods", status_code=303)


@router.get("/edit/{pm_id}", name="edit_payment_method")
def edit_payment_method(request: Request, pm_id: int):
    pm = get_payment_method_by_id(pm_id)
    if not pm:
        return RedirectResponse(url="/payment_methods", status_code=302)
    return templates.TemplateResponse(request, "payment_methods/form.html", {"pm": pm})


@router.post("/edit/{pm_id}", name="update_payment_method")
def update_payment_method_post(
    pm_id: int,
    descripcion: str = Form(...),
    nombre: str = Form(""),
):
    update_payment_method(pm_id, descripcion, nombre)
    return RedirectResponse(url="/payment_methods", status_code=303)


@router.get("/delete/{pm_id}", name="delete_payment_method")
def delete_payment_method_get(pm_id: int):
    delete_payment_method(pm_id)
    return RedirectResponse(url="/payment_methods", status_code=302)
