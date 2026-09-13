from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Houmba H API"
    app_env: str = "development"
    database_url: str = "sqlite:///./houmba.db"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    ai_provider: str = "openai_compatible"
    ai_base_url: str = "https://api.openai.com/v1"
    ai_api_key: str = ""
    ai_model: str = "gpt-4o-mini"
    ai_timeout_seconds: float = 45.0
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
