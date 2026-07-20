from app.utils.file_hashing import compute_sha256


def test_same_content_produces_same_hash():
    content = b"contenido de prueba"
    assert compute_sha256(content) == compute_sha256(content)


def test_different_content_produces_different_hash():
    assert compute_sha256(b"documento uno") != compute_sha256(b"documento dos")
