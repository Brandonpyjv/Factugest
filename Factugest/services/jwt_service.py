import os
from datetime import datetime, timedelta, timezone

from jose import jwt

JWT_SECRET = os.getenv("JWT_SECRET", "factugest-jwt-dev-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "24"))


def create_access_token(payload: dict, expires_hours: int | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=expires_hours or JWT_EXPIRE_HOURS)
    return jwt.encode({**payload, "exp": expire}, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
