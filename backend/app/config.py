from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./data/grants.db"

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # Gemini API
    gemini_api_key: str

    # Groq API
    groq_api_key: str

    # Grants.gov API
    grants_gov_api_key: str = ""

    # Scraping
    scraper_user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    scraper_schedule_cron: str = "0 2 * * 0"

    # File Storage
    upload_dir: str = "./data/uploads"
    generated_dir: str = "./data/generated"
    max_upload_size_mb: int = 10

    # Development
    debug: bool = True
    cors_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
