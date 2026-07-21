from app.rag.intent import classify_intent, is_goodbye, is_gratitude, is_greeting


def test_detects_simple_greetings():
    assert is_greeting("Hola")
    assert is_greeting("Buenos días")
    assert is_greeting("buenas tardes")
    assert is_greeting("Buenas noches!")


def test_detects_compound_greetings():
    assert is_greeting("Hola, ¿cómo estás?")
    assert is_greeting("Hola, buenos días")
    assert is_greeting("Hola, buenas tardes")
    assert is_greeting("Buenas")
    assert is_greeting("Buenas noches")
    assert is_greeting("Hola, necesito ayuda")


def test_detects_gratitude():
    assert is_gratitude("Gracias")
    assert is_gratitude("muchas gracias")
    assert is_gratitude("gracias por la ayuda")
    assert is_gratitude("excelente gracias")


def test_detects_goodbye():
    assert is_goodbye("Adiós")
    assert is_goodbye("hasta luego")
    assert is_goodbye("nos vemos")


def test_does_not_detect_real_questions():
    assert not is_greeting("Hola, ¿cuál es el horario de atención?")
    assert not is_gratitude("Hola, ¿cuál es el horario de atención?")
    assert not is_goodbye("Hola, ¿cuál es el horario de atención?")
    assert not is_greeting("¿Cuáles son las políticas de vacaciones de la empresa?")
    assert not is_greeting("Necesito el protocolo de incidentes")
    assert not is_gratitude("Necesito el protocolo de incidentes")
    assert not is_greeting("Buenas tardes, necesito el protocolo de incidentes")


def test_classify_intent():
    assert classify_intent("Hola") == "greeting"
    assert classify_intent("Gracias") == "gratitude"
    assert classify_intent("Adiós") == "goodbye"
    assert classify_intent("¿Cuál es el horario de atención?") == "question"
