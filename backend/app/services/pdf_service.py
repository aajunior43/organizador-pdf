import os
import uuid
import asyncio
from typing import List, Optional, Dict, Any
from pathlib import Path
import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageDraw, ImageFont
import pytesseract
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import logging

from ..core.config import settings
from ..models.pdf_project import PDFProject, PDFFile, PDFOperation
from ..utils.file_utils import ensure_directory, get_file_hash

logger = logging.getLogger(__name__)

class PDFService:
    """Serviço principal para operações com PDF"""
    
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.output_dir = Path(settings.OUTPUT_DIR)
        self.temp_dir = Path(settings.TEMP_DIR)
        
        # Garantir que os diretórios existem
        for directory in [self.upload_dir, self.output_dir, self.temp_dir]:
            ensure_directory(directory)
    
    async def save_uploaded_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Salva arquivo enviado e extrai metadados"""
        try:
            # Gerar nome único para o arquivo
            file_id = str(uuid.uuid4())
            file_extension = Path(filename).suffix
            stored_filename = f"{file_id}{file_extension}"
            file_path = self.upload_dir / stored_filename
            
            # Salvar arquivo
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            # Extrair metadados
            metadata = await self.extract_pdf_metadata(file_path)
            
            # Gerar thumbnail
            thumbnail_path = await self.generate_thumbnail(file_path, file_id)
            
            return {
                "file_id": file_id,
                "original_filename": filename,
                "stored_filename": stored_filename,
                "file_path": str(file_path),
                "file_size": len(file_content),
                "thumbnail_path": thumbnail_path,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo {filename}: {str(e)}")
            raise
    
    async def extract_pdf_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extrai metadados do PDF"""
        try:
            # Usar PyMuPDF para metadados detalhados
            doc = fitz.open(str(file_path))
            metadata = doc.metadata
            
            # Usar PyPDF2 para informações adicionais
            with open(file_path, "rb") as f:
                pdf_reader = PdfReader(f)
                page_count = len(pdf_reader.pages)
                
                # Extrair texto da primeira página para preview
                first_page_text = ""
                if page_count > 0:
                    first_page_text = pdf_reader.pages[0].extract_text()[:500]
            
            doc.close()
            
            return {
                "page_count": page_count,
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
                "producer": metadata.get("producer", ""),
                "creation_date": metadata.get("creationDate", ""),
                "modification_date": metadata.get("modDate", ""),
                "first_page_text": first_page_text,
                "file_size_mb": round(file_path.stat().st_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair metadados: {str(e)}")
            return {"page_count": 0, "error": str(e)}
    
    async def generate_thumbnail(self, file_path: Path, file_id: str) -> Optional[str]:
        """Gera thumbnail da primeira página do PDF"""
        try:
            doc = fitz.open(str(file_path))
            page = doc[0]  # Primeira página
            
            # Renderizar página como imagem
            mat = fitz.Matrix(settings.PREVIEW_DPI / 72, settings.PREVIEW_DPI / 72)
            pix = page.get_pixmap(matrix=mat)
            
            # Converter para PIL Image
            img_data = pix.tobytes("ppm")
            img = Image.open(BytesIO(img_data))
            
            # Redimensionar para thumbnail
            img.thumbnail(settings.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            
            # Salvar thumbnail
            thumbnail_filename = f"{file_id}_thumb.png"
            thumbnail_path = self.temp_dir / thumbnail_filename
            img.save(thumbnail_path, "PNG")
            
            doc.close()
            return str(thumbnail_path)
            
        except Exception as e:
            logger.error(f"Erro ao gerar thumbnail: {str(e)}")
            return None
    
    async def merge_pdfs(self, pdf_files: List[PDFFile], output_filename: str) -> Dict[str, Any]:
        """Mescla múltiplos PDFs em um único arquivo"""
        try:
            pdf_writer = PdfWriter()
            total_pages = 0
            
            # Ordenar arquivos por order_index
            sorted_files = sorted(pdf_files, key=lambda x: x.order_index)
            
            for pdf_file in sorted_files:
                with open(pdf_file.file_path, "rb") as f:
                    pdf_reader = PdfReader(f)
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
                        total_pages += 1
            
            # Salvar arquivo mesclado
            output_path = self.output_dir / output_filename
            with open(output_path, "wb") as output_file:
                pdf_writer.write(output_file)
            
            return {
                "success": True,
                "output_path": str(output_path),
                "total_pages": total_pages,
                "file_size": output_path.stat().st_size
            }
            
        except Exception as e:
            logger.error(f"Erro ao mesclar PDFs: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def compress_pdf(self, input_path: str, output_path: str, quality: int = 85) -> Dict[str, Any]:
        """Comprime um PDF reduzindo o tamanho"""
        try:
            doc = fitz.open(input_path)
            
            # Aplicar compressão
            doc.save(output_path, garbage=4, deflate=True, clean=True)
            
            original_size = Path(input_path).stat().st_size
            compressed_size = Path(output_path).stat().st_size
            compression_ratio = round((1 - compressed_size / original_size) * 100, 2)
            
            doc.close()
            
            return {
                "success": True,
                "original_size": original_size,
                "compressed_size": compressed_size,
                "compression_ratio": compression_ratio
            }
            
        except Exception as e:
            logger.error(f"Erro ao comprimir PDF: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def extract_text_ocr(self, pdf_path: str) -> Dict[str, Any]:
        """Extrai texto do PDF usando OCR"""
        try:
            if not settings.OCR_ENABLED:
                return {"success": False, "error": "OCR não está habilitado"}
            
            doc = fitz.open(pdf_path)
            extracted_text = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Renderizar página como imagem
                mat = fitz.Matrix(2, 2)  # Aumentar resolução para melhor OCR
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("ppm")
                img = Image.open(BytesIO(img_data))
                
                # Aplicar OCR
                text = pytesseract.image_to_string(img, lang=settings.OCR_LANGUAGE)
                extracted_text.append({
                    "page": page_num + 1,
                    "text": text.strip()
                })
            
            doc.close()
            
            return {
                "success": True,
                "pages": extracted_text,
                "total_pages": len(extracted_text)
            }
            
        except Exception as e:
            logger.error(f"Erro no OCR: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def add_watermark(self, pdf_path: str, watermark_text: str, output_path: str) -> Dict[str, Any]:
        """Adiciona marca d'água ao PDF"""
        try:
            # Criar PDF com marca d'água
            watermark_buffer = BytesIO()
            c = canvas.Canvas(watermark_buffer, pagesize=letter)
            
            # Configurar texto da marca d'água
            c.setFont("Helvetica", 50)
            c.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.3)
            c.rotate(45)
            c.drawString(200, 200, watermark_text)
            c.save()
            
            # Aplicar marca d'água a todas as páginas
            watermark_buffer.seek(0)
            watermark_pdf = PdfReader(watermark_buffer)
            watermark_page = watermark_pdf.pages[0]
            
            with open(pdf_path, "rb") as f:
                pdf_reader = PdfReader(f)
                pdf_writer = PdfWriter()
                
                for page in pdf_reader.pages:
                    page.merge_page(watermark_page)
                    pdf_writer.add_page(page)
                
                with open(output_path, "wb") as output_file:
                    pdf_writer.write(output_file)
            
            return {"success": True, "output_path": output_path}
            
        except Exception as e:
            logger.error(f"Erro ao adicionar marca d'água: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def split_pdf(self, pdf_path: str, output_dir: str, pages_per_file: int = 1) -> Dict[str, Any]:
        """Divide um PDF em múltiplos arquivos"""
        try:
            with open(pdf_path, "rb") as f:
                pdf_reader = PdfReader(f)
                total_pages = len(pdf_reader.pages)
                
                output_files = []
                
                for i in range(0, total_pages, pages_per_file):
                    pdf_writer = PdfWriter()
                    
                    # Adicionar páginas ao novo PDF
                    for j in range(i, min(i + pages_per_file, total_pages)):
                        pdf_writer.add_page(pdf_reader.pages[j])
                    
                    # Salvar arquivo dividido
                    output_filename = f"split_{i//pages_per_file + 1}.pdf"
                    output_path = Path(output_dir) / output_filename
                    
                    with open(output_path, "wb") as output_file:
                        pdf_writer.write(output_file)
                    
                    output_files.append(str(output_path))
                
                return {
                    "success": True,
                    "output_files": output_files,
                    "total_files": len(output_files)
                }
                
        except Exception as e:
            logger.error(f"Erro ao dividir PDF: {str(e)}")
            return {"success": False, "error": str(e)}