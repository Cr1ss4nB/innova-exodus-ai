from functools import lru_cache

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import get_settings


@lru_cache
def get_embeddings_model() -> GoogleGenerativeAIEmbeddings:
    """Retorna el modelo de embeddings de Gemini, configurado según el .env."""
    settings = get_settings()
    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.gemini_api_key,
        output_dimensionality=settings.embedding_dimension,
    )
