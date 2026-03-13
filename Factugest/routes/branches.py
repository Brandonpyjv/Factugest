from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from services.branches import (get_all_branches, get_branch_by_id,
                                create_branch, update_branch, delete_branch)
from templates_config import templates

router = APIRouter(prefix="/branches")


@router.get("", name="branches")
def branches(request: Request):
    data = get_all_branches()
    return templates.TemplateResponse(request, "branches/index.html", {"branches": data})


@router.get("/new", name="new_branch")
def new_branch(request: Request):
    return templates.TemplateResponse(request, "branches/form.html", {"branch": None})


@router.post("/new", name="create_branch")
def create_branch_post(
    nombre: str = Form(...),
    nit: str = Form(...),
    dv: str = Form(""),
    direccion: str = Form(""),
    ciudad: str = Form(""),
    telefono: str = Form(""),
    correo: str = Form(""),
    regimen_tributario: str = Form("RESPONSABLE_IVA"),
    actividad_economica: str = Form(""),
    tipo_documento: str = Form("NIT"),
):
    create_branch(nombre, nit, dv, direccion, ciudad, telefono, correo,
                  regimen_tributario, actividad_economica, tipo_documento)
    return RedirectResponse(url="/branches", status_code=303)


@router.get("/edit/{branch_id}", name="edit_branch")
def edit_branch(request: Request, branch_id: int):
    branch = get_branch_by_id(branch_id)
    if not branch:
        return RedirectResponse(url="/branches", status_code=302)
    return templates.TemplateResponse(request, "branches/form.html", {"branch": branch})


@router.post("/edit/{branch_id}", name="update_branch")
def update_branch_post(
    branch_id: int,
    nombre: str = Form(...),
    nit: str = Form(...),
    dv: str = Form(""),
    direccion: str = Form(""),
    ciudad: str = Form(""),
    telefono: str = Form(""),
    correo: str = Form(""),
    regimen_tributario: str = Form("RESPONSABLE_IVA"),
    actividad_economica: str = Form(""),
    tipo_documento: str = Form("NIT"),
):
    update_branch(branch_id, nombre, nit, dv, direccion, ciudad, telefono, correo,
                  regimen_tributario, actividad_economica, tipo_documento)
    return RedirectResponse(url="/branches", status_code=303)


@router.get("/delete/{branch_id}", name="delete_branch")
def delete_branch_get(branch_id: int):
    delete_branch(branch_id)
    return RedirectResponse(url="/branches", status_code=302)
