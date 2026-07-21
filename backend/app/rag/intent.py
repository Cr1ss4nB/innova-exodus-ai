import re
import unicodedata

def _normalize(text: str) -> str:
    """Normaliza texto: minúsculas, sin acentos, sin signos de puntuación, sin espacios extra."""
    text = text.strip().lower()
    text = "".join(char for char in unicodedata.normalize("NFKD", text) if not unicodedata.combining(char))
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


GREETING_PHRASES = {
    "hola",
    "hola!",
    "holi",
    "holas",
    "que onda",
    "holis",
    "hola chatbot",
    "hola bot",
    "buenas",
    "buenas!",
    "buenos dias",
    "buen día",
    "buen dia",
    "buenas tardes",
    "buenas noches",
    "que tal",
    "qué tal",
    "como estas",
    "cómo estás",
    "como va",
    "cómo va",
    "como te va",
    "cómo te va",
    "como andas",
    "cómo andas",
    "como vas",
    "cómo vas",
    "que hay",
    "qué hay",
    "que hubo",
    "qué hubo",
    "que mas",
    "qué más",
    "todo bien",
    "todo bien?",
    "todo bien contigo",
    "hey",
    "hey!",
    "ey",
    "hi",
    "hello",
    "saludos",
    "un saludo",
    "muy buenas",
    "buenas gente",
    "necesito ayuda",
    "ayuda",
    "me ayudas",
    "me puedes ayudar",
    "puedes ayudarme",
    "quiero hacer una consulta",
    "tengo una consulta",
    "tengo una pregunta",
    "puedo hacerte una pregunta",
    "necesito informacion",
    "necesito información",
    "quiero informacion",
    "quiero información",
    "alguien ahi",
    "alguien ahí",
}

GRATITUDE_PHRASES = {
    "gracias",
    "muchas gracias",
    "muchisimas gracias",
    "muchísimas gracias",
    "mil gracias",
    "te lo agradezco",
    "te agradezco",
    "agradecido",
    "agradecida",
    "gracias por tu ayuda",
    "gracias por ayudarme",
    "gracias por la informacion",
    "gracias por la información",
    "excelente gracias",
    "perfecto gracias",
    "genial gracias",
    "muy amable",
    "eres muy amable",
    "se agradece",
    "thanks",
    "thank you",
    "de nada",
    "no hay de que",
    "no hay de qué",
}

GRATITUDE_KEYWORDS = {
    "gracias",
    "agradezco",
    "agradecido",
    "agradecida",
    "thanks",
    "thank",
}

GOODBYE_PHRASES = {
    "adios",
    "adiós",
    "hasta luego",
    "hasta pronto",
    "hasta la proxima",
    "hasta la próxima",
    "hasta mañana",
    "nos vemos",
    "nos vemos luego",
    "nos vemos pronto",
    "chao",
    "chau",
    "bye",
    "goodbye",
    "hasta despues",
    "hasta después",
    "me voy",
    "eso es todo",
    "eso seria todo",
    "eso sería todo",
    "terminamos",
    "listo gracias",
    "listo muchas gracias",
    "ya no necesito mas",
    "ya no necesito más",
    "nos hablamos",
    "que tengas un buen dia",
    "que tengas un buen día",
    "que tengas buena tarde",
    "que tengas buena noche",
    "hasta otra",
    "hasta otra ocasión",
    "adios y gracias",
    "adiós y gracias",
}

GOODBYE_KEYWORDS = {
    "adios",
    "adiós",
    "chao",
    "chau",
    "bye",
    "goodbye",
}

GOODBYE_KEYWORD_PHRASES = {
    "nos vemos",
    "nos vemos luego",
    "nos vemos pronto",
    "hasta luego",
    "hasta pronto",
    "hasta la proxima",
    "hasta la próxima",
    "hasta mañana",
    "hasta otra",
    "hasta otra ocasión",
    "me voy",
    "eso es todo",
    "eso seria todo",
    "eso sería todo",
    "ya no necesito mas",
    "ya no necesito más",
}

GREETING_PHRASES = {_normalize(p) for p in GREETING_PHRASES}
GRATITUDE_PHRASES = {_normalize(p) for p in GRATITUDE_PHRASES}
GOODBYE_PHRASES = {_normalize(p) for p in GOODBYE_PHRASES}

GRATITUDE_KEYWORDS = {_normalize(k) for k in GRATITUDE_KEYWORDS}
GOODBYE_KEYWORDS = {_normalize(k) for k in GOODBYE_KEYWORDS}
GOODBYE_KEYWORD_PHRASES = {_normalize(p) for p in GOODBYE_KEYWORD_PHRASES}

MAX_FILLER_WORDS = 7


def _segments(message: str) -> list[str]:
    """Divide un mensaje por pausas comunes."""
    parts = re.split(r"[,.;!]+", message)
    return [part.strip() for part in parts if part.strip()]

def _contains_only_social_words(message: str) -> bool:
    """Detecta si un mensaje contiene únicamente saludos, agradecimientos o despedidas, incluso si combina varias frases 
    separadas por coma, punto y coma o punto."""
    normalized = _normalize(message)

    if not normalized:
        return False

    phrase_sets = (
        GREETING_PHRASES,
        GRATITUDE_PHRASES,
        GOODBYE_PHRASES,
    )

    text = normalized

    changed = True
    while changed:
        changed = False

        for phrases in phrase_sets:
            for phrase in sorted(phrases, key=len, reverse=True):
                if phrase in text:
                    text = text.replace(phrase, " ")
                    changed = True

        text = re.sub(r"\s+", " ", text).strip()

    return text == ""

def _is_short_filler(segment: str, keywords: set[str], keyword_phrases: set[str] = frozenset()) -> bool:
    """Reconoce variantes cortas de una intención (por ejemplo, 'gracias por la ayuda'), sin
    confundirlas con preguntas reales: exige que no haya signo de interrogación y que el
    segmento sea corto."""
    if "?" in segment or "¿" in segment:
        return False

    normalized = _normalize(segment)
    words = normalized.split()

    if not words or len(words) > MAX_FILLER_WORDS:
        return False

    if any(word in keywords for word in words):
        return True

    return any(phrase in normalized for phrase in keyword_phrases)


def _all_segments_recognized(
    message: str,
    phrase_set: set[str],
    keywords: set[str] = frozenset(),
    keyword_phrases: set[str] = frozenset(),
) -> bool:
    segments = _segments(message)
    if not segments:
        return False

    for segment in segments:
        if _normalize(segment) in phrase_set:
            continue
        if keywords and _is_short_filler(segment, keywords, keyword_phrases):
            continue
        return False

    return True


def is_greeting(message: str) -> bool:
    """Detecta si un mensaje es únicamente un saludo, incluso si combina varias frases separadas por coma."""
    return _all_segments_recognized(message, GREETING_PHRASES)


def is_gratitude(message: str) -> bool:
    """Detecta agradecimientos, incluyendo variantes cortas como 'gracias por la ayuda'."""
    return _all_segments_recognized(message, GRATITUDE_PHRASES, keywords=GRATITUDE_KEYWORDS)


def is_goodbye(message: str) -> bool:
    """Detecta despedidas, incluyendo variantes cortas."""
    return _all_segments_recognized(
        message, GOODBYE_PHRASES, keywords=GOODBYE_KEYWORDS, keyword_phrases=GOODBYE_KEYWORD_PHRASES
    )


def classify_intent(message: str) -> str:
    """
    Clasifica un mensaje como greeting, gratitude, goodbye o question.
    También reconoce combinaciones como: hola gracias, hola muchas gracias, hola adios
    """

    if is_greeting(message):
        return "greeting"

    if is_gratitude(message):
        return "gratitude"

    if is_goodbye(message):
        return "goodbye"

    if _contains_only_social_words(message):
        normalized = _normalize(message)

        if any(p in normalized for p in GOODBYE_PHRASES):
            return "goodbye"

        if any(p in normalized for p in GRATITUDE_PHRASES):
            return "gratitude"

        return "greeting"

    return "question"