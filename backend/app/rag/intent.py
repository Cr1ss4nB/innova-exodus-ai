import re
import unicodedata

GREETING_PHRASES = {
    "hola",
    "buenas",
    "buenos dias",
    "buenos días",
    "buenas tardes",
    "buenas noches",
    "buen dia",
    "que tal",
    "como estas",
    "hey",
    "gracias",
    "muchas gracias",
    "mil gracias",
    "de nada",
    "adios",
    "hasta luego",
    "nos vemos",
    "chao",
    "hasta pronto",
    "nos vemos pronto",
}


def _normalize(text: str) -> str:
    """Normaliza texto: minúsculas, sin acentos, sin signos de puntuación, sin espacios extra."""
    text = text.strip().lower()
    text = "".join(char for char in unicodedata.normalize("NFKD", text) if not unicodedata.combining(char))
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_greeting(message: str) -> bool:
    """Detecta si un mensaje es únicamente un saludo o cortesía, sin contenido de consulta."""
    return _normalize(message) in GREETING_PHRASES
