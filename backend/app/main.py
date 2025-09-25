from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import List, Optional
from contextlib import asynccontextmanager
import os
import uuid
import shutil
from pathlib import Path
from datetime import datetime
import traceback

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 PDF Organizer API iniciada")
    logger.info(f"📁 Diretório de upload: {settings.UPLOAD_DIR}")
    logger.info(f"📁 Diretório de saída: {settings.OUTPUT_DIR}")
    yield
    # Shutdown
    logger.info("🛑 PDF Organizer API encerrada")

# Criar instância do FastAPI
app = FastAPI(
    title="PDF Organizer API",
    description="API moderna para organização e manipulação de arquivos PDF",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de requests HTTP"""
    start_time = datetime.utcnow()
    request_id = str(uuid.uuid4())[:8]

    # Log do request
    logger.info(
        f"[{request_id}] {request.method} {request.url} - "
        f"User-Agent: {request.headers.get('user-agent', 'Unknown')}"
    )

    # Processar request
    try:
        response = await call_next(request)
        process_time = (datetime.utcnow() - start_time).total_seconds()

        # Log da resposta
        logger.info(
            f"[{request_id}] {response.status_code} - "
            f"Processado em {process_time:.4f}s"
        )

        # Adicionar headers de resposta
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)

        return response

    except Exception as exc:
        process_time = (datetime.utcnow() - start_time).total_seconds()
        logger.error(
            f"[{request_id}] ERRO - {str(exc)} - "
            f"Tempo até erro: {process_time:.4f}s"
        )
        raise

# Criar diretórios necessários
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
os.makedirs(settings.TEMP_DIR, exist_ok=True)

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.mount("/outputs", StaticFiles(directory=settings.OUTPUT_DIR), name="outputs")

# Adicionar manipuladores de erro globais
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manipulador para erros de validação de request"""
    logger.error(f"Erro de validação: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Dados inválidos fornecidos",
            "errors": exc.errors(),
            "message": "Por favor, verifique os dados enviados"
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Manipulador para exceções HTTP"""
    logger.error(f"Erro HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "message": "Ocorreu um erro ao processar sua solicitação"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Manipulador para exceções gerais"""
    logger.error(f"Erro interno: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Erro interno do servidor",
            "message": "Ocorreu um erro inesperado. Tente novamente mais tarde.",
            "error_id": str(uuid.uuid4())  # ID único para rastreamento
        }
    )

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )