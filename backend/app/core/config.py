import secrets
from functools import lru_cache
from typing import List, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore",
        case_sensitive=False
    )

    # App settings
    app_name: str = "Nautix API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = Field(default="development", pattern="^(development|staging|production)$")

    # Database
    database_url: str = "sqlite:///./nautix.db"

    # Security
    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins_raw: str = "*"
    cors_allow_credentials: bool = True

    # JWT keys for QR tokens
    jwt_private_key_path: str = "keys/qr_es256_private.pem"
    jwt_public_key_path: str = "keys/qr_es256_public.pem"

    # External services
    stripe_secret_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None

    @property
    def cors_origins(self) -> List[str]:
        raw = self.cors_origins_raw
        if not raw or raw.strip() == "*":
            return ["*"]
        return [o.strip() for o in raw.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
