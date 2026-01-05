import jwt
from datetime import datetime, timedelta, timezone
from config import settings

def create_access_token(data: dict):
    access_token = create_token(data.id, data.role, token_type=settings.access_cookie_name, expires_minutes = settings.access_token_expires_minutes)
    return access_token


def create_token(user_id, role, token_type, expires_minutes):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "role": str(role),
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
        "iss": settings.app_name,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_token(token: str, expected_type: str) -> dict:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != expected_type:
            raise jwt.InvalidTokenError("Invalid token type")
        return payload