from pathlib import Path


def save_file_bytes(destination: Path, content: bytes) -> int:
    """Escribe el contenido en disco, creando el directorio si no existe, y retorna los bytes escritos."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    return len(content)


def delete_file(path: Path) -> None:
    """Elimina un archivo del disco si existe."""
    if path.exists():
        path.unlink()
