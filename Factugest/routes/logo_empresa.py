"""
El logo que va en el membrete de cada empresa emisora.

Va aparte del formulario de la empresa por la misma razón que la foto de perfil:
subir un archivo obliga a que todo el formulario viaje como `multipart`, y ese
formulario tiene veinte campos que ya funcionan. Una pantalla propia para una
cosa propia.

**Cada emisor lleva el suyo.** Antes el PDF tenía escrito el logo de FactuGest y
lo estampaba en todos los documentos, también en los que emitimos por cuenta de
terceros: la factura de una clínica salía con nuestra marca. Un documento fiscal
dice quién lo expidió, y el membrete es parte de esa afirmación.
"""
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse

from database import execute_update
from services import auditoria_service as auditoria
from services.avatar_service import FotoInvalidaError, eliminar_logo, guardar_logo
from services.branches import get_branch_by_id
from templates_config import templates

router = APIRouter(prefix="/branches")


def _guardar(cod_empresa: int, nombre):
    return execute_update("UPDATE empresas SET logo = %s WHERE cod_empresa = %s",
                          (nombre, cod_empresa))


@router.get("/{branch_id}/logo", name="branch_logo_form")
def logo_form(request: Request, branch_id: int, error: str = ""):
    empresa = get_branch_by_id(branch_id)
    if not empresa:
        return RedirectResponse(url="/branches", status_code=302)
    return templates.TemplateResponse(request, "branches/logo.html", {
        "empresa": empresa,
        "error": error,
    })


@router.post("/{branch_id}/logo", name="branch_logo_save")
async def logo_save(request: Request, branch_id: int, logo: UploadFile = File(...)):
    empresa = get_branch_by_id(branch_id)
    if not empresa:
        return RedirectResponse(url="/branches", status_code=303)

    try:
        nombre = guardar_logo(await logo.read(), branch_id)
    except FotoInvalidaError as e:
        return RedirectResponse(url=f"/branches/{branch_id}/logo?error={e}",
                                status_code=303)

    eliminar_logo(empresa.get("logo"))
    _guardar(branch_id, nombre)
    auditoria.registrar(request, "ACTUALIZO", "empresa", branch_id,
                        f"Cambió el logo de {empresa['nombre']}")
    return RedirectResponse(url=f"/branches/{branch_id}/logo", status_code=303)


@router.post("/{branch_id}/logo/eliminar", name="branch_logo_delete")
def logo_delete(request: Request, branch_id: int):
    empresa = get_branch_by_id(branch_id)
    if empresa:
        eliminar_logo(empresa.get("logo"))
        _guardar(branch_id, None)
        auditoria.registrar(request, "ACTUALIZO", "empresa", branch_id,
                            f"Quitó el logo de {empresa['nombre']}; el membrete "
                            "vuelve a mostrar el nombre")
    return RedirectResponse(url=f"/branches/{branch_id}/logo", status_code=303)
