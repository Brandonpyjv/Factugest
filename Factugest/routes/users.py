from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from typing import Optional
from services.user_service import get_all_users, get_user_by_id, create_user, update_user, delete_user
from services.branches import get_all_branches
from auth import can_manage, ROLE_HIERARCHY
from templates_config import templates

router = APIRouter(prefix="/users")

# Roles que un actor puede asignar, filtrados por jerarquía
def _assignable_roles(actor_rol: str) -> list:
    actor_level = ROLE_HIERARCHY.get(actor_rol, 0)
    order = ["ADMIN", "JEFE_TIENDA", "SUPERVISOR", "CAJERO"]
    labels = {
        "ADMIN": "Administrador",
        "JEFE_TIENDA": "Jefe de Tienda",
        "SUPERVISOR": "Supervisor",
        "CAJERO": "Cajero",
    }
    return [
        {"value": r, "label": labels[r]}
        for r in order
        if ROLE_HIERARCHY[r] < actor_level
    ]


@router.get("", name="users")
def users(request: Request):
    actor = request.session.get("user", {})
    data = get_all_users()
    return templates.TemplateResponse(request, "users/index.html", {
        "usuarios": data,
        "actor_rol": actor.get("rol", ""),
    })


@router.get("/new", name="new_user")
def new_user(request: Request):
    actor = request.session.get("user", {})
    roles = _assignable_roles(actor.get("rol", ""))
    return templates.TemplateResponse(request, "users/form.html", {
        "user": None,
        "empresas": get_all_branches(),
        "roles_disponibles": roles,
    })


@router.post("/new", name="create_user")
def create_user_post(
    request: Request,
    nombre: str = Form(...),
    correo: str = Form(...),
    contrasena: str = Form(...),
    rol: str = Form(...),
    cod_empresa: Optional[int] = Form(None),
):
    actor = request.session.get("user", {})
    if not can_manage(actor.get("rol", ""), rol):
        return RedirectResponse(url="/users", status_code=303)
    create_user(nombre, correo, contrasena, rol, cod_empresa)
    return RedirectResponse(url="/users", status_code=303)


@router.get("/edit/{user_id}", name="edit_user")
def edit_user(request: Request, user_id: int):
    actor = request.session.get("user", {})
    user = get_user_by_id(user_id)
    if not user or not can_manage(actor.get("rol", ""), user.get("rol", "")):
        return RedirectResponse(url="/users", status_code=302)
    roles = _assignable_roles(actor.get("rol", ""))
    return templates.TemplateResponse(request, "users/form.html", {
        "user": user,
        "empresas": get_all_branches(),
        "roles_disponibles": roles,
    })


@router.post("/edit/{user_id}", name="update_user")
def update_user_post(
    request: Request,
    user_id: int,
    nombre: str = Form(...),
    correo: str = Form(...),
    rol: str = Form(...),
    contrasena: str = Form(""),
    cod_empresa: Optional[int] = Form(None),
):
    actor = request.session.get("user", {})
    target = get_user_by_id(user_id)
    if not target or not can_manage(actor.get("rol", ""), target.get("rol", "")):
        return RedirectResponse(url="/users", status_code=303)
    if not can_manage(actor.get("rol", ""), rol):
        return RedirectResponse(url="/users", status_code=303)
    update_user(user_id, nombre, correo, rol, contrasena if contrasena else None, cod_empresa)
    return RedirectResponse(url="/users", status_code=303)


@router.get("/delete/{user_id}", name="delete_user")
def delete_user_get(request: Request, user_id: int):
    actor = request.session.get("user", {})
    target = get_user_by_id(user_id)
    if not target or not can_manage(actor.get("rol", ""), target.get("rol", "")):
        return RedirectResponse(url="/users", status_code=302)
    delete_user(user_id)
    return RedirectResponse(url="/users", status_code=302)
