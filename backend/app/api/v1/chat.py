from fastapi import APIRouter, HTTPException, status

from app.core.exceptions import ChatError, EmbeddingGenerationError, VectorStoreError
from app.schemas.chat_schemas import ChatRequest, ChatResponse
from app.services.chat_service import ask

router = APIRouter(prefix="/chat")


@router.post("", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """Responde una pregunta utilizando exclusivamente la documentación indexada en FAISS."""
    try:
        chat_answer = ask(request.question)
    except (EmbeddingGenerationError, VectorStoreError) as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(error)) from error
    except ChatError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(error)) from error

    return ChatResponse.from_answer(chat_answer)
