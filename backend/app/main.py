from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path
from datetime import datetime

from .core.config import settings
from .core.security import get_current_user
from .api import pdf_router, auth_router, user_router
from .services.pdf_service import PDFService
from .models.database import engine, Base
from .utils.logger import setup_logger

# Criar tabelas do banco de dados
Base.metadata.create_all(bind=engine)

# Configurar logger
logger = setup_logger(__name__)

# Criar instância do FastAPI
app = FastAPI(
    title="PDF Organizer API",
    description="API moderna para organização e manipulação de arquivos PDF",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar diretórios necessários
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
os.makedirs(settings.TEMP_DIR, exist_ok=True)

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.mount("/outputs", StaticFiles(directory=settings.OUTPUT_DIR), name="outputs")

# Incluir routers
app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user_router.router, prefix="/api/users", tags=["Users"])
app.include_router(pdf_router.router, prefix="/api/pdf", tags=["PDF Operations"])

@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "PDF Organizer API v3.0",
        "status": "online",
        "docs": "/docs",
        "features": [
            "Upload múltiplo de PDFs",
            "Organização por drag-and-drop",
            "Preview de páginas",
            "Mesclagem de PDFs",
            "OCR e extração de texto",
            "Compressão de PDFs",
            "Watermark e assinatura digital",
            "Autenticação de usuários",
            "Histórico de operações"
        ]
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "version": "3.0.0",
        "timestamp": str(datetime.utcnow())
    }

@app.on_event("startup")
async def startup_event():
    """Eventos de inicialização"""
    logger.info("🚀 PDF Organizer API iniciada")
    logger.info(f"📁 Diretório de upload: {settings.UPLOAD_DIR}")
    logger.info(f"📁 Diretório de saída: {settings.OUTPUT_DIR}")

@app.on_event("shutdown")
async def shutdown_event():
    """Eventos de encerramento"""
    logger.info("🛑 PDF Organizer API encerrada")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )