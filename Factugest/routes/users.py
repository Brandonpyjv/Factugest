from fastapi import APIRouter, Request
from services.user_service import get_all_users
from templates_config import templates

router = APIRouter()


@router.get("/users", name="users")
def users(request: Request):
    data = get_all_users()
    return templates.TemplateResponse(request, "users/index.html", {"usuarios": data})


@router.get("/users/new", name="new_user")
def new_user(request: Request):
    return templates.TemplateResponse(request, "users/form.html")
