from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    """Verifica que el servicio esté disponible."""
    settings = get_settings()
    return {"status": "ok", "app_name": settings.app_name}
