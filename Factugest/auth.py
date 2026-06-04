import bcrypt
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

_PUBLIC_PREFIXES = (
    "/login",
    "/static",
    "/api/v1/",     # endpoints JSON nuevos: autenticados vía JWT, no por sesión
    "/docs",        # Swagger UI
    "/redoc",       # ReDoc UI
    "/openapi.json",
)

# Roles con permisos completos de administración
ADMIN_ROLES = {"ADMIN", "SUPERVISOR", "JEFE_TIENDA"}

# Jerarquía de roles: mayor número = mayor autoridad
ROLE_HIERARCHY = {
    "ADMIN":       4,
    "JEFE_TIENDA": 3,
    "SUPERVISOR":  2,
    "CAJERO":      1,
}


def role_level(rol: str) -> int:
    return ROLE_HIERARCHY.get(rol, 0)


def can_manage(actor_rol: str, target_rol: str) -> bool:
    """Retorna True si actor_rol puede crear/editar/eliminar a target_rol."""
    return role_level(actor_rol) > role_level(target_rol)

# Rutas exclusivas de roles admin (bloqueadas para CAJERO)
_ADMIN_ONLY_PREFIXES = (
    "/users", "/logs", "/branches",
    "/payment_methods", "/invoice_taxes", "/invoice_payments",
)

# Acciones de escritura bloqueadas para CAJERO
_CAJERO_BLOCKED_PREFIXES = (
    "/product/new", "/product/edit", "/product/delete",
    "/discount/new", "/discount/edit", "/discount/delete",
    "/invoice/delete",
)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    if not hashed.startswith("$2"):
        return plain == hashed
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def get_session_user(request: Request):
    return request.session.get("user")


def is_admin(user: dict) -> bool:
    return user.get("rol") in ADMIN_ROLES


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if any(path.startswith(p) for p in _PUBLIC_PREFIXES):
            return await call_next(request)

        user = request.session.get("user")
        if not user:
            return RedirectResponse("/login", status_code=302)

        rol = user.get("rol")

        # Rutas solo para roles admin
        if any(path.startswith(p) for p in _ADMIN_ONLY_PREFIXES):
            if rol not in ADMIN_ROLES:
                return RedirectResponse("/", status_code=302)

        # Acciones de escritura bloqueadas para CAJERO
        if rol == "CAJERO" and any(path.startswith(p) for p in _CAJERO_BLOCKED_PREFIXES):
            return RedirectResponse("/", status_code=302)

        return await call_next(request)
