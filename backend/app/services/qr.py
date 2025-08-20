from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt

from app.core.config import settings


def _read_key(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def sign_qr_token(payload: Dict[str, Any], expires_minutes: int = 60 * 24) -> str:
    to_encode = payload.copy()
    to_encode.update({
        "iat": int(datetime.utcnow().timestamp()),
        "exp": int((datetime.utcnow() + timedelta(minutes=expires_minutes)).timestamp()),
    })

    private_key = _read_key(settings.jwt_private_key_path)
    token = jwt.encode(to_encode, private_key, algorithm="ES256")
    return token


def verify_qr_token(token: str) -> Dict[str, Any]:
    public_key = _read_key(settings.jwt_public_key_path)
    data = jwt.decode(token, public_key, algorithms=["ES256"])
    return data

