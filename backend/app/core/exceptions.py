class DocumentProcessingError(Exception):
    """Error base para fallos durante el procesamiento de un documento."""


class InvalidPDFError(DocumentProcessingError):
    """El archivo no pudo abrirse como un PDF válido."""


class EmptyPDFError(DocumentProcessingError):
    """El PDF no contiene texto extraíble."""


class EmbeddingGenerationError(DocumentProcessingError):
    """Fallo al generar embeddings para uno o más fragmentos."""


class VectorStoreError(DocumentProcessingError):
    """Error al operar sobre el índice vectorial FAISS."""


class InvalidUploadError(DocumentProcessingError):
    """El archivo subido no cumple con las restricciones de carga permitidas."""


class DocumentNotFoundError(DocumentProcessingError):
    """No existe un documento registrado con el id solicitado."""


class ChatError(Exception):
    """Error base para fallos durante el flujo de consulta del chat."""


class LLMGenerationError(ChatError):
    """Fallo al generar una respuesta con el modelo de lenguaje."""
