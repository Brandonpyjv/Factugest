from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from typing import Optional
from services.user_service import get_all_users, get_user_by_id, create_user, update_user, delete_user
from services.branches import get_all_branches
from templates_config import templates

router = APIRouter(prefix="/users")


@router.get("", name="users")
def users(request: Request):
    data = get_all_users()
    return templates.TemplateResponse(request, "users/index.html", {"usuarios": data})


@router.get("/new", name="new_user")
def new_user(request: Request):
    return templates.TemplateResponse(request, "users/form.html", {
        "user": None,
        "empresas": get_all_branches(),
    })


@router.post("/new", name="create_user")
def create_user_post(
    nombre: str = Form(...),
    correo: str = Form(...),
    contrasena: str = Form(...),
    rol: str = Form(...),
    cod_empresa: Optional[int] = Form(None),
):
    create_user(nombre, correo, contrasena, rol, cod_empresa)
    return RedirectResponse(url="/users", status_code=303)


@router.get("/edit/{user_id}", name="edit_user")
def edit_user(request: Request, user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        return RedirectResponse(url="/users", status_code=302)
    return templates.TemplateResponse(request, "users/form.html", {
        "user": user,
        "empresas": get_all_branches(),
    })


@router.post("/edit/{user_id}", name="update_user")
def update_user_post(
    user_id: int,
    nombre: str = Form(...),
    correo: str = Form(...),
    rol: str = Form(...),
    contrasena: str = Form(""),
    cod_empresa: Optional[int] = Form(None),
):
    update_user(user_id, nombre, correo, rol, contrasena if contrasena else None, cod_empresa)
    return RedirectResponse(url="/users", status_code=303)


@router.get("/delete/{user_id}", name="delete_user")
def delete_user_get(user_id: int):
    delete_user(user_id)
    return RedirectResponse(url="/users", status_code=302)
