from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from typing import Optional
from services.branches import (get_all_branches, get_branch_by_id,
                                create_branch, update_branch, delete_branch)
from services.ubicacion_service import get_all_departamentos, get_municipios_by_departamento
from templates_config import templates

router = APIRouter(prefix="/branches")


@router.get("", name="branches")
def branches(request: Request):
    data = get_all_branches()
    return templates.TemplateResponse(request, "branches/index.html", {"branches": data})


@router.get("/new", name="new_branch")
def new_branch(request: Request):
    return templates.TemplateResponse(request, "branches/form.html", {
        "branch": None,
        "departamentos": get_all_departamentos(),
        "municipios": [],
    })


@router.post("/new", name="create_branch")
def create_branch_post(
    nombre: str = Form(...),
    nit: str = Form(...),
    dv: str = Form(""),
    direccion: str = Form(""),
    cod_municipio: str = Form(""),
    telefono: str = Form(""),
    correo: str = Form(""),
    regimen_tributario: str = Form("RESPONSABLE_IVA"),
    actividad_economica: str = Form(""),
    tipo_documento: str = Form("NIT"),
    website: str = Form(""),
    tarifa_ica: str = Form(""),
    autoretenedor: int = Form(0),
    gran_contribuyente: int = Form(0),
    prefijo_factura: str = Form("FV"),
    resolucion_dian: str = Form(""),
    resolucion_fecha_desde: Optional[str] = Form(None),
    resolucion_fecha_hasta: Optional[str] = Form(None),
    resolucion_desde: Optional[str] = Form(None),
    resolucion_hasta: Optional[str] = Form(None),
    consecutivo_actual: Optional[str] = Form("1"),
):
    create_branch(nombre, nit, dv, direccion, cod_municipio, telefono, correo,
                  regimen_tributario, actividad_economica, tipo_documento,
                  website, tarifa_ica, autoretenedor, gran_contribuyente,
                  prefijo_factura, resolucion_dian, resolucion_fecha_desde,
                  resolucion_fecha_hasta,
                  int(resolucion_desde) if resolucion_desde else None,
                  int(resolucion_hasta) if resolucion_hasta else None,
                  int(consecutivo_actual) if consecutivo_actual else 1)
    return RedirectResponse(url="/branches", status_code=303)


@router.get("/edit/{branch_id}", name="edit_branch")
def edit_branch(request: Request, branch_id: int):
    branch = get_branch_by_id(branch_id)
    if not branch:
        return RedirectResponse(url="/branches", status_code=302)
    municipios = []
    if branch.get("cod_departamento"):
        municipios = get_municipios_by_departamento(branch["cod_departamento"])
    return templates.TemplateResponse(request, "branches/form.html", {
        "branch": branch,
        "departamentos": get_all_departamentos(),
        "municipios": municipios,
    })


@router.post("/edit/{branch_id}", name="update_branch")
def update_branch_post(
    branch_id: int,
    nombre: str = Form(...),
    nit: str = Form(...),
    dv: str = Form(""),
    direccion: str = Form(""),
    cod_municipio: str = Form(""),
    telefono: str = Form(""),
    correo: str = Form(""),
    regimen_tributario: str = Form("RESPONSABLE_IVA"),
    actividad_economica: str = Form(""),
    tipo_documento: str = Form("NIT"),
    website: str = Form(""),
    tarifa_ica: str = Form(""),
    autoretenedor: int = Form(0),
    gran_contribuyente: int = Form(0),
    prefijo_factura: str = Form("FV"),
    resolucion_dian: str = Form(""),
    resolucion_fecha_desde: Optional[str] = Form(None),
    resolucion_fecha_hasta: Optional[str] = Form(None),
    resolucion_desde: Optional[str] = Form(None),
    resolucion_hasta: Optional[str] = Form(None),
    consecutivo_actual: Optional[str] = Form("1"),
):
    update_branch(branch_id, nombre, nit, dv, direccion, cod_municipio, telefono, correo,
                  regimen_tributario, actividad_economica, tipo_documento,
                  website, tarifa_ica, autoretenedor, gran_contribuyente,
                  prefijo_factura, resolucion_dian, resolucion_fecha_desde,
                  resolucion_fecha_hasta,
                  int(resolucion_desde) if resolucion_desde else None,
                  int(resolucion_hasta) if resolucion_hasta else None,
                  int(consecutivo_actual) if consecutivo_actual else 1)
    return RedirectResponse(url="/branches", status_code=303)


@router.get("/delete/{branch_id}", name="delete_branch")
def delete_branch_get(branch_id: int):
    delete_branch(branch_id)
    return RedirectResponse(url="/branches", status_code=302)
