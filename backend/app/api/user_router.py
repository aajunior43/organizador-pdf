from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..models.database import get_db
from ..models.user import User
from ..core.security import get_current_active_user, get_password_hash
from ..utils.schemas import UserResponse, UserUpdate, PasswordChange

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Obtém informações do usuário atual"""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Atualiza informações do usuário atual"""
    # Verificar se email já está em uso por outro usuário
    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está em uso"
            )
    
    # Atualizar campos
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.post("/me/change-password")
async def change_password(
    password_change: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Altera senha do usuário"""
    from ..core.security import verify_password
    
    # Verificar senha atual
    if not verify_password(password_change.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta"
        )
    
    # Atualizar senha
    current_user.hashed_password = get_password_hash(password_change.new_password)
    db.commit()
    
    return {"message": "Senha alterada com sucesso"}

@router.delete("/me")
async def delete_current_user(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Exclui conta do usuário atual"""
    db.delete(current_user)
    db.commit()
    
    return {"message": "Conta excluída com sucesso"}

@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtém estatísticas do usuário"""
    from ..models.pdf_project import PDFProject, PDFOperation
    
    # Contar projetos
    total_projects = db.query(PDFProject).filter(
        PDFProject.owner_id == current_user.id
    ).count()
    
    # Contar operações
    total_operations = db.query(PDFOperation).filter(
        PDFOperation.user_id == current_user.id
    ).count()
    
    # Operações por tipo
    operations_by_type = db.query(
        PDFOperation.operation_type,
        db.func.count(PDFOperation.id)
    ).filter(
        PDFOperation.user_id == current_user.id
    ).group_by(PDFOperation.operation_type).all()
    
    return {
        "total_projects": total_projects,
        "total_operations": total_operations,
        "operations_by_type": dict(operations_by_type),
        "member_since": current_user.created_at.isoformat() if current_user.created_at else None
    }