import re
import unicodedata

GREETING_PHRASES = {
    "hola", "buenas", "buenos dias", "buenas tardes", "buenas noches", "buen dia", "que tal", "como estas", "hey", "gracias",
    "muchas gracias", "mil gracias", "de nada", "adios", "hasta luego", "nos vemos", "chao", "necesito ayuda", "que onda",
    "tengo una duda", "tengo una pregunta", "puedes ayudarme", "ayuda por favor", "soporte", "asistencia", "hola hola""buenas buenas", "holis", 
    "holi", "que mas", "como va", "como vais", "que hay", "aló"
}


def _normalize(text: str) -> str:
    """Normaliza texto: minúsculas, sin acentos, sin signos de puntuación, sin espacios extra."""
    text = text.strip().lower()
    text = "".join(char for char in unicodedata.normalize("NFKD", text) if not unicodedata.combining(char))
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_greeting(message: str) -> bool:
    """Detecta si un mensaje es únicamente un saludo o cortesía, incluso si combina
    varias frases de saludo separadas por coma (por ejemplo, "Hola, buenos días")."""
    segments = [segment.strip() for segment in message.split(",")]
    segments = [segment for segment in segments if segment]

    if not segments:
        return False

    return all(_normalize(segment) in GREETING_PHRASES for segment in segments)
