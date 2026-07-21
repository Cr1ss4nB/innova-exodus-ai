from app.rag.intent import is_greeting


def test_detects_simple_greetings():
    assert is_greeting("Hola")
    assert is_greeting("Buenos días")
    assert is_greeting("buenas tardes")
    assert is_greeting("Buenas noches!")
    assert is_greeting("Gracias")
    assert is_greeting("muchas gracias")


def test_detects_compound_greetings():
    assert is_greeting("Hola, ¿cómo estás?")
    assert is_greeting("Hola, buenos días")
    assert is_greeting("Hola, buenas tardes")
    assert is_greeting("Buenas")
    assert is_greeting("Buenas noches")
    assert is_greeting("Hola, necesito ayuda")


def test_does_not_detect_real_questions():
    assert not is_greeting("Hola, ¿cuál es el horario de atención?")
    assert not is_greeting("¿Cuáles son las políticas de vacaciones de la empresa?")
    assert not is_greeting("Necesito el protocolo de incidentes")
    assert not is_greeting("Buenas tardes, necesito el protocolo de incidentes")
