from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

# Schemas de usuário
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Senha deve ter pelo menos 8 caracteres')
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Nova senha deve ter pelo menos 8 caracteres')
        return v

# Schemas de autenticação
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: Optional[Dict[str, Any]] = None

class TokenData(BaseModel):
    username: Optional[str] = None

# Schemas de projeto PDF
class PDFProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False
    settings: Optional[Dict[str, Any]] = None

class PDFProjectCreate(PDFProjectBase):
    pass

class PDFProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    settings: Optional[Dict[str, Any]] = None

class PDFProjectResponse(PDFProjectBase):
    id: int
    owner_id: int
    status: str
    output_filename: Optional[str] = None
    output_path: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schemas de arquivo PDF
class PDFFileBase(BaseModel):
    original_filename: str
    order_index: int = 0

class PDFFileResponse(PDFFileBase):
    id: int
    project_id: int
    stored_filename: str
    file_path: str
    file_size: int
    page_count: Optional[int] = None
    thumbnail_path: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas de operação PDF
class PDFOperationBase(BaseModel):
    operation_type: str
    parameters: Optional[Dict[str, Any]] = None

class PDFOperationResponse(PDFOperationBase):
    id: int
    user_id: int
    project_id: Optional[int] = None
    status: str
    input_files: Optional[List[str]] = None
    output_files: Optional[List[str]] = None
    error_message: Optional[str] = None
    processing_time: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schemas de requisições específicas
class MergePDFRequest(BaseModel):
    output_filename: str
    
    @validator('output_filename')
    def validate_filename(cls, v):
        if not v.endswith('.pdf'):
            v += '.pdf'
        return v

class CompressPDFRequest(BaseModel):
    input_file_id: int
    quality: int = 85
    output_filename: str
    
    @validator('quality')
    def validate_quality(cls, v):
        if not 1 <= v <= 100:
            raise ValueError('Qualidade deve estar entre 1 e 100')
        return v

class WatermarkRequest(BaseModel):
    input_file_id: int
    watermark_text: str
    output_filename: str
    opacity: float = 0.3
    font_size: int = 50
    rotation: int = 45
    
    @validator('opacity')
    def validate_opacity(cls, v):
        if not 0.1 <= v <= 1.0:
            raise ValueError('Opacidade deve estar entre 0.1 e 1.0')
        return v

class SplitPDFRequest(BaseModel):
    input_file_id: int
    pages_per_file: int = 1
    output_prefix: str = "split"
    
    @validator('pages_per_file')
    def validate_pages_per_file(cls, v):
        if v < 1:
            raise ValueError('Páginas por arquivo deve ser pelo menos 1')
        return v

class OCRRequest(BaseModel):
    input_file_id: int
    language: str = "por+eng"
    output_format: str = "text"  # text, json

# Schemas de resposta
class FileUploadResponse(BaseModel):
    message: str
    files: List[PDFFileResponse]
    total_files: int
    total_size: int

class OperationStatusResponse(BaseModel):
    operation_id: int
    status: str
    progress: Optional[int] = None
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

class ProjectStatsResponse(BaseModel):
    total_files: int
    total_pages: int
    total_size: int
    file_types: Dict[str, int]
    last_modified: Optional[datetime] = None

# Schemas de configuração
class AppSettings(BaseModel):
    max_file_size: int
    max_files_per_upload: int
    allowed_extensions: List[str]
    supported_operations: List[str]
    ocr_enabled: bool
    ocr_languages: List[str]