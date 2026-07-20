from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación, cargada desde variables de entorno."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    gemini_api_key: str
    model_name: str = "gemini-3.1-flash-lite"
    app_name: str = "Innova Exodus Assistant"

    embedding_model: str = "gemini-embedding-001"
    embedding_dimension: int = 768

    host: str = "0.0.0.0"
    port: int = 8000

    chunk_size: int = 1000
    chunk_overlap: int = 150

    temperature: float = 0.1
    top_k: int = 5

    cors_origins: str = "http://localhost:5500"

    vector_store_dir: str = "data/vector_store"

    @property
    def cors_origins_list(self) -> list[str]:
        """Convierte el string de orígenes separados por coma en una lista."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Retorna la instancia de configuración, cacheada por proceso."""
    return Settings()
