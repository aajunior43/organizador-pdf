import os
import hashlib
import shutil
from pathlib import Path
from typing import Optional

def ensure_directory(directory: Path) -> None:
    """Garante que o diretório existe"""
    directory.mkdir(parents=True, exist_ok=True)

def get_file_hash(file_path: Path) -> str:
    """Calcula hash MD5 do arquivo"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_file_size_mb(file_path: Path) -> float:
    """Retorna tamanho do arquivo em MB"""
    return round(file_path.stat().st_size / (1024 * 1024), 2)

def clean_filename(filename: str) -> str:
    """Remove caracteres inválidos do nome do arquivo"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def copy_file(source: Path, destination: Path) -> bool:
    """Copia arquivo de origem para destino"""
    try:
        ensure_directory(destination.parent)
        shutil.copy2(source, destination)
        return True
    except Exception:
        return False

def move_file(source: Path, destination: Path) -> bool:
    """Move arquivo de origem para destino"""
    try:
        ensure_directory(destination.parent)
        shutil.move(str(source), str(destination))
        return True
    except Exception:
        return False

def delete_file(file_path: Path) -> bool:
    """Exclui arquivo"""
    try:
        if file_path.exists():
            file_path.unlink()
        return True
    except Exception:
        return False

def get_available_space(directory: Path) -> int:
    """Retorna espaço disponível em bytes"""
    statvfs = os.statvfs(directory)
    return statvfs.f_frsize * statvfs.f_bavail

def cleanup_temp_files(temp_dir: Path, max_age_hours: int = 24) -> int:
    """Remove arquivos temporários antigos"""
    import time
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    deleted_count = 0
    
    for file_path in temp_dir.rglob('*'):
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                try:
                    file_path.unlink()
                    deleted_count += 1
                except Exception:
                    pass
    
    return deleted_count