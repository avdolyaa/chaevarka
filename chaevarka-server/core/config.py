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

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_prefix="TEA_",
    )
    run: RunConfig
    db: DatabaseConfig

settings = Settings()
