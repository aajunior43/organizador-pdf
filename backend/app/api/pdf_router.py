from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from typing import List, Optional
from sqlalchemy.orm import Session
import os
import uuid
from pathlib import Path

from ..models.database import get_db
from ..models.user import User
from ..models.pdf_project import PDFProject, PDFFile, PDFOperation
from ..core.security import get_current_active_user
from ..services.pdf_service import PDFService
from ..core.config import settings
from ..utils.schemas import (
    PDFProjectCreate, PDFProjectResponse, PDFFileResponse,
    PDFOperationResponse, MergePDFRequest, CompressPDFRequest,
    WatermarkRequest, SplitPDFRequest
)

router = APIRouter()
pdf_service = PDFService()

@router.post("/projects/", response_model=PDFProjectResponse)
async def create_project(
    project: PDFProjectCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cria um novo projeto PDF"""
    db_project = PDFProject(
        name=project.name,
        description=project.description,
        owner_id=current_user.id,
        is_public=project.is_public,
        settings=project.settings
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/projects/", response_model=List[PDFProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Lista projetos do usuário"""
    projects = db.query(PDFProject).filter(
        PDFProject.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return projects

@router.get("/projects/{project_id}", response_model=PDFProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtém um projeto específico"""
    project = db.query(PDFProject).filter(
        PDFProject.id == project_id,
        PDFProject.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    return project

@router.post("/projects/{project_id}/upload", response_model=List[PDFFileResponse])
async def upload_files(
    project_id: int,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload de arquivos PDF para um projeto"""
    # Verificar se o projeto existe e pertence ao usuário
    project = db.query(PDFProject).filter(
        PDFProject.id == project_id,
        PDFProject.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    # Validar arquivos
    if len(files) > settings.MAX_FILES_PER_UPLOAD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Máximo de {settings.MAX_FILES_PER_UPLOAD} arquivos por upload"
        )
    
    uploaded_files = []
    
    for file in files:
        # Validar extensão
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Arquivo {file.filename} não é um PDF válido"
            )
        
        # Validar tamanho
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Arquivo {file.filename} excede o tamanho máximo"
            )
        
        # Salvar arquivo
        file_info = await pdf_service.save_uploaded_file(content, file.filename)
        
        # Criar registro no banco
        db_file = PDFFile(
            project_id=project_id,
            original_filename=file_info["original_filename"],
            stored_filename=file_info["stored_filename"],
            file_path=file_info["file_path"],
            file_size=file_info["file_size"],
            page_count=file_info["metadata"].get("page_count", 0),
            thumbnail_path=file_info["thumbnail_path"],
            metadata=file_info["metadata"],
            order_index=len(uploaded_files)
        )
        
        db.add(db_file)
        uploaded_files.append(db_file)
    
    db.commit()
    
    # Refresh para obter IDs
    for file in uploaded_files:
        db.refresh(file)
    
    return uploaded_files

@router.put("/projects/{project_id}/reorder")
async def reorder_files(
    project_id: int,
    file_orders: List[dict],  # [{"file_id": 1, "order_index": 0}, ...]
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Reordena arquivos em um projeto"""
    project = db.query(PDFProject).filter(
        PDFProject.id == project_id,
        PDFProject.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    # Atualizar ordem dos arquivos
    for item in file_orders:
        db.query(PDFFile).filter(
            PDFFile.id == item["file_id"],
            PDFFile.project_id == project_id
        ).update({"order_index": item["order_index"]})
    
    db.commit()
    return {"message": "Ordem dos arquivos atualizada"}

@router.post("/projects/{project_id}/merge")
async def merge_project_pdfs(
    project_id: int,
    request: MergePDFRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mescla todos os PDFs de um projeto"""
    project = db.query(PDFProject).filter(
        PDFProject.id == project_id,
        PDFProject.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    # Obter arquivos do projeto
    pdf_files = db.query(PDFFile).filter(
        PDFFile.project_id == project_id
    ).order_by(PDFFile.order_index).all()
    
    if not pdf_files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum arquivo PDF encontrado no projeto"
        )
    
    # Criar operação
    operation = PDFOperation(
        user_id=current_user.id,
        project_id=project_id,
        operation_type="merge",
        status="processing",
        parameters={"output_filename": request.output_filename}
    )
    db.add(operation)
    db.commit()
    db.refresh(operation)
    
    try:
        # Mesclar PDFs
        result = await pdf_service.merge_pdfs(pdf_files, request.output_filename)
        
        if result["success"]:
            # Atualizar projeto
            project.output_filename = request.output_filename
            project.output_path = result["output_path"]
            project.status = "completed"
            
            # Atualizar operação
            operation.status = "completed"
            operation.output_files = [result["output_path"]]
            
            db.commit()
            
            return {
                "message": "PDFs mesclados com sucesso",
                "output_path": result["output_path"],
                "total_pages": result["total_pages"],
                "operation_id": operation.id
            }
        else:
            operation.status = "error"
            operation.error_message = result["error"]
            db.commit()
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
            
    except Exception as e:
        operation.status = "error"
        operation.error_message = str(e)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/projects/{project_id}/download")
async def download_project_output(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Download do arquivo final do projeto"""
    project = db.query(PDFProject).filter(
        PDFProject.id == project_id,
        PDFProject.owner_id == current_user.id
    ).first()
    
    if not project or not project.output_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo de saída não encontrado"
        )
    
    if not os.path.exists(project.output_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo não existe no sistema"
        )
    
    return FileResponse(
        path=project.output_path,
        filename=project.output_filename,
        media_type="application/pdf"
    )

@router.post("/compress")
async def compress_pdf(
    request: CompressPDFRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Comprime um PDF"""
    # Implementar compressão de PDF
    pass

@router.post("/watermark")
async def add_watermark(
    request: WatermarkRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Adiciona marca d'água a um PDF"""
    # Implementar marca d'água
    pass

@router.post("/split")
async def split_pdf(
    request: SplitPDFRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Divide um PDF em múltiplos arquivos"""
    # Implementar divisão de PDF
    pass

@router.get("/operations/", response_model=List[PDFOperationResponse])
async def list_operations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Lista operações do usuário"""
    operations = db.query(PDFOperation).filter(
        PDFOperation.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return operations