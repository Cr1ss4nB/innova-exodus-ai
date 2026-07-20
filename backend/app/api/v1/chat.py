from fastapi import APIRouter

from app.schemas.chat_schemas import ChatRequest, ChatResponse
from app.services.chat_service import ask

router = APIRouter(prefix="/chat")


@router.post("", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """Responde una pregunta utilizando exclusivamente la documentación indexada en FAISS."""
    chat_answer = ask(request.question)
    return ChatResponse.from_answer(chat_answer)
