from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "sqlite:///./nautix.db"

    # CORS
    cors_origins_raw: str = "*"

    # JWT keys for QR tokens
    jwt_private_key_path: str = "keys/qr_es256_private.pem"
    jwt_public_key_path: str = "keys/qr_es256_public.pem"

    # Stripe (optional in dev)
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None

    @property
    def cors_origins(self) -> List[str]:
        raw = self.cors_origins_raw
        if not raw:
            return ["*"]
        if raw.strip() == "*":
            return ["*"]
        return [o.strip() for o in raw.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

