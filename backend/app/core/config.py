from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Configuración de la aplicación, cargada desde variables de entorno."""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"), env_file_encoding="utf-8", extra="ignore"
    )

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
    uploads_dir: str = "data/uploads"
    max_upload_size_mb: int = 20

    @property
    def cors_origins_list(self) -> list[str]:
        """Convierte el string de orígenes separados por coma en una lista."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def vector_store_path(self) -> Path:
        """Ruta absoluta del directorio del índice vectorial, sin depender del directorio de ejecución."""
        return BASE_DIR / self.vector_store_dir

    @property
    def uploads_path(self) -> Path:
        """Ruta absoluta del directorio de archivos subidos, sin depender del directorio de ejecución."""
        return BASE_DIR / self.uploads_dir

    @property
    def documents_registry_path(self) -> Path:
        """Ruta absoluta del archivo de registro de documentos."""
        return BASE_DIR / "data" / "documents_registry.json"


@lru_cache
def get_settings() -> Settings:
    """Retorna la instancia de configuración, cacheada por proceso."""
    return Settings()
