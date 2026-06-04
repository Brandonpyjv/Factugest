from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import JWTError

from auth import verify_password
from services.user_service import get_user_by_email, get_user_by_id
from services.jwt_service import create_access_token, decode_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["auth (mobile)"])

bearer_scheme = HTTPBearer()


class LoginRequest(BaseModel):
    correo: str
    contrasena: str


class UserOut(BaseModel):
    cod_usuario: int
    nombre: str
    correo: str
    rol: str
    cod_empresa: int | None = None
    empresa_nombre: str | None = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


def _user_to_out(user: dict) -> UserOut:
    return UserOut(
        cod_usuario=user["cod_usuario"],
        nombre=user["nombre"],
        correo=user["correo"],
        rol=user["rol"],
        cod_empresa=user.get("cod_empresa"),
        empresa_nombre=user.get("empresa_nombre"),
    )


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    user = get_user_by_email(payload.correo)
    if (
        not user
        or not user.get("activo", 1)
        or not verify_password(payload.contrasena, user["contrasena"])
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({
        "sub": str(user["cod_usuario"]),
        "rol": user["rol"],
        "cod_empresa": user.get("cod_empresa"),
        "nombre": user["nombre"],
    })

    return LoginResponse(access_token=token, user=_user_to_out(user))


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(creds.credentials)
    except JWTError:
        raise credentials_exc

    cod_usuario_str = payload.get("sub")
    if not cod_usuario_str:
        raise credentials_exc

    user = get_user_by_id(int(cod_usuario_str))
    if not user or not user.get("activo", 1):
        raise credentials_exc

    return user


@router.get("/me", response_model=UserOut)
def me(user: dict = Depends(get_current_user)):
    return _user_to_out(user)
