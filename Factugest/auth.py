import bcrypt
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Rutas públicas que no requieren autenticación
_PUBLIC_PREFIXES = ("/login", "/static")
# Rutas solo para ADMIN
_ADMIN_PREFIXES = ("/users", "/logs")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    # Contraseña aún en texto plano (no hasheada con BCrypt)
    if not hashed.startswith("$2"):
        return plain == hashed
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def get_session_user(request: Request):
    return request.session.get("user")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if any(path.startswith(p) for p in _PUBLIC_PREFIXES):
            return await call_next(request)

        user = request.session.get("user")
        if not user:
            return RedirectResponse("/login", status_code=302)

        if any(path.startswith(p) for p in _ADMIN_PREFIXES):
            if user.get("rol") != "ADMIN":
                return RedirectResponse("/", status_code=302)

        return await call_next(request)
