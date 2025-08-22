from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Configurações básicas
    APP_NAME: str = "PDF Organizer"
    VERSION: str = "3.0.0"
    DEBUG: bool = True
    
    # Configurações do servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Configurações de CORS
    ALLOWED_HOSTS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]
    
    # Configurações de banco de dados
    DATABASE_URL: str = "sqlite:///./pdf_organizer.db"
    
    # Configurações de segurança
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configurações de arquivos
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    UPLOAD_DIR: str = str(BASE_DIR / "uploads")
    OUTPUT_DIR: str = str(BASE_DIR / "outputs")
    TEMP_DIR: str = str(BASE_DIR / "temp")
    STATIC_DIR: str = str(BASE_DIR / "static")
    
    # Configurações de upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf"]
    MAX_FILES_PER_UPLOAD: int = 20
    
    # Configurações de PDF
    PDF_QUALITY: int = 85
    THUMBNAIL_SIZE: tuple = (200, 280)
    PREVIEW_DPI: int = 150
    
    # Configurações de OCR
    OCR_ENABLED: bool = True
    OCR_LANGUAGE: str = "por+eng"
    
    # Configurações de Redis (para cache e filas)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Configurações de email (para notificações)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    # Configurações de logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "pdf_organizer.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instância global das configurações
settings = Settings()

# Criar diretórios necessários
for directory in [settings.UPLOAD_DIR, settings.OUTPUT_DIR, settings.TEMP_DIR, settings.STATIC_DIR]:
    os.makedirs(directory, exist_ok=True)