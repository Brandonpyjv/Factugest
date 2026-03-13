from fastapi import APIRouter, Request
from services.branches import get_all_branches
from templates_config import templates

router = APIRouter()


@router.get("/branches", name="branches")
def branches(request: Request):
    data = get_all_branches()
    return templates.TemplateResponse(request, "branches/index.html", {"branches": data})


@router.get("/new_branch", name="new_branch")
def new_branch(request: Request):
    return templates.TemplateResponse(request, "branches/form.html")
