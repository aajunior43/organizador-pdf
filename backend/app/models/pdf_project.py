from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class PDFProject(Base):
    """Modelo de projeto PDF"""
    __tablename__ = "pdf_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=False)
    status = Column(String(50), default="draft")  # draft, processing, completed, error
    output_filename = Column(String(255), nullable=True)
    output_path = Column(String(500), nullable=True)
    settings = Column(JSON, nullable=True)  # Configurações específicas do projeto
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    owner = relationship("User", back_populates="pdf_projects")
    pdf_files = relationship("PDFFile", back_populates="project", cascade="all, delete-orphan")
    operations = relationship("PDFOperation", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<PDFProject(id={self.id}, name='{self.name}', owner_id={self.owner_id})>"

class PDFFile(Base):
    """Modelo de arquivo PDF"""
    __tablename__ = "pdf_files"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("pdf_projects.id"), nullable=False)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    page_count = Column(Integer, nullable=True)
    order_index = Column(Integer, default=0)
    thumbnail_path = Column(String(500), nullable=True)
    metadata = Column(JSON, nullable=True)  # Metadados do PDF
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    project = relationship("PDFProject", back_populates="pdf_files")
    
    def __repr__(self):
        return f"<PDFFile(id={self.id}, filename='{self.original_filename}', project_id={self.project_id})>"

class PDFOperation(Base):
    """Modelo de operação PDF (histórico)"""
    __tablename__ = "pdf_operations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("pdf_projects.id"), nullable=True)
    operation_type = Column(String(50), nullable=False)  # merge, split, compress, ocr, watermark, etc.
    status = Column(String(50), default="pending")  # pending, processing, completed, error
    input_files = Column(JSON, nullable=True)  # Lista de arquivos de entrada
    output_files = Column(JSON, nullable=True)  # Lista de arquivos de saída
    parameters = Column(JSON, nullable=True)  # Parâmetros da operação
    error_message = Column(Text, nullable=True)
    processing_time = Column(Integer, nullable=True)  # Tempo em segundos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    user = relationship("User", back_populates="pdf_operations")
    project = relationship("PDFProject", back_populates="operations")
    
    def __repr__(self):
        return f"<PDFOperation(id={self.id}, type='{self.operation_type}', status='{self.status}')>"