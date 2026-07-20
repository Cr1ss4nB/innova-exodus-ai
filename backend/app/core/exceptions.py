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
