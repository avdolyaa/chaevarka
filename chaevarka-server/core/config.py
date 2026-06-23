from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


BASE_DIR = Path(__file__).resolve().parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False

class ApiConfig(BaseModel):
    prefix: str = "/api/v1"

class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str

class SuperuserConfig(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str

class SmtpConfig(BaseModel):
    host: str = "maildev"
    port: int = 1025
    username: str = ""
    password: str = ""
    from_email: str = "noreply@teavibe.site"
    use_tls: bool = False

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="TEA_",
    )
    run: RunConfig
    db: DatabaseConfig
    api: ApiConfig = ApiConfig()
    access_token: AccessToken
    superuser: SuperuserConfig
    docs_password: str = ""
    smtp: SmtpConfig = SmtpConfig()


settings = Settings()
