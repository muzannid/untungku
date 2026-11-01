"""Application settings, loaded from environment variables / the .env file."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Root of the backend project (the folder that contains `app/`).
BASE_DIR = Path(__file__).resolve().parents[2]

# Default local database: a SQLite file inside the backend folder, so the API
# boots with zero setup and works no matter which directory it is started from.
DEFAULT_DATABASE_URL = f"sqlite:///{(BASE_DIR / 'untungku.db').as_posix()}"

DEFAULT_CORS_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- Application ---
    PROJECT_NAME: str = "UntungKu API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # --- Auth (used by the upcoming auth module) ---
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # --- Database ---
    # SQLite for local development. Point this at PostgreSQL for deployment:
    #   postgresql://user:password@host:5432/untungku_db
    DATABASE_URL: str = DEFAULT_DATABASE_URL

    # Comma-separated list, e.g. "http://localhost:5173,https://untungku.vercel.app"
    BACKEND_CORS_ORIGINS: str = DEFAULT_CORS_ORIGINS

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
