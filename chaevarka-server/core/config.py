from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)



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
    superuser_email: str
    superuser_password: str
    superuser_first_name: str
    superuser_last_name: str
    superuser_phone: str


settings = Settings()
