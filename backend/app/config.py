from typing import List

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    supabase_url: str = Field(
        default="https://fdeilubldzcjzerbpkdgss.supabase.co",
        validation_alias=AliasChoices("SUPABASE_URL", "supabase_url"),
    )
    supabase_anon_key: str = Field(
        default="",
        validation_alias=AliasChoices("SUPABASE_ANON_KEY", "supabase_anon_key"),
    )
    supabase_service_role: str = Field(
        default="",
        validation_alias=AliasChoices("SUPABASE_SERVICE_ROLE", "supabase_service_role"),
    )
    jwt_secret: str = Field(
        default="smart-ai-forecasting-secret-key",
        validation_alias=AliasChoices("JWT_SECRET", "jwt_secret"),
    )
    jwt_algorithm: str = Field(
        default="HS256",
        validation_alias=AliasChoices("JWT_ALGORITHM", "jwt_algorithm"),
    )
    jwt_expiration_hours: int = Field(
        default=24,
        validation_alias=AliasChoices("JWT_EXPIRATION_HOURS", "jwt_expiration_hours"),
    )
    host: str = Field(
        default="0.0.0.0",
        validation_alias=AliasChoices("HOST", "host"),
    )
    port: int = Field(
        default=8001,
        validation_alias=AliasChoices("PORT", "port"),
    )
    cors_origins: List[str] = Field(
        default=["http://localhost:8000", "http://localhost:3000", "*"],
        validation_alias=AliasChoices("CORS_ORIGINS", "cors_origins"),
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            import json
            try:
                return json.loads(value)
            except Exception:
                return [item.strip() for item in value.split(",") if item.strip()]
        return value


settings = Settings()
