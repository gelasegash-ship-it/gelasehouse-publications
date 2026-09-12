from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Houmba H API"
    app_env: str = "development"
    database_url: str = "sqlite:///./houmba.db"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    ai_provider: str = ""
    ai_api_key: str = ""
    ai_model: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
