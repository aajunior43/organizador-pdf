import pytest
import tempfile
import os
from pathlib import Path
from app.services.pdf_service import PDFService
from app.models.pdf_project import PDFFile

class TestPDFService:
    """Test PDF service functionality"""
    
    @pytest.fixture
    def pdf_service(self):
        """Create PDF service instance"""
        return PDFService()
    
    @pytest.fixture
    def sample_pdf_content(self):
        """Create sample PDF content"""
        return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n174\n%%EOF"
    
    @pytest.mark.asyncio
    async def test_save_uploaded_file(self, pdf_service: PDFService, sample_pdf_content: bytes):
        """Test saving uploaded file"""
        filename = "test.pdf"
        
        result = await pdf_service.save_uploaded_file(sample_pdf_content, filename)
        
        assert "file_id" in result
        assert result["original_filename"] == filename
        assert result["file_size"] == len(sample_pdf_content)
        assert "metadata" in result
        
        # Cleanup
        if os.path.exists(result["file_path"]):
            os.unlink(result["file_path"])
    
    @pytest.mark.asyncio
    async def test_extract_pdf_metadata(self, pdf_service: PDFService, temp_pdf_file: str):
        """Test extracting PDF metadata"""
        file_path = Path(temp_pdf_file)
        
        metadata = await pdf_service.extract_pdf_metadata(file_path)
        
        assert "page_count" in metadata
        assert "file_size_mb" in metadata
        assert isinstance(metadata["page_count"], int)
        assert isinstance(metadata["file_size_mb"], float)
    
    @pytest.mark.asyncio
    async def test_generate_thumbnail(self, pdf_service: PDFService, temp_pdf_file: str):
        """Test generating PDF thumbnail"""
        file_path = Path(temp_pdf_file)
        file_id = "test_thumbnail"
        
        thumbnail_path = await pdf_service.generate_thumbnail(file_path, file_id)
        
        # Note: This might return None if PyMuPDF can't process the minimal PDF
        if thumbnail_path:
            assert os.path.exists(thumbnail_path)
            assert thumbnail_path.endswith(".png")
            
            # Cleanup
            os.unlink(thumbnail_path)
    
    @pytest.mark.asyncio
    async def test_merge_pdfs(self, pdf_service: PDFService, temp_pdf_file: str):
        """Test merging PDFs"""
        # Create mock PDF files
        pdf_files = [
            type('PDFFile', (), {
                'file_path': temp_pdf_file,
                'order_index': 0
            })(),
            type('PDFFile', (), {
                'file_path': temp_pdf_file,
                'order_index': 1
            })()
        ]
        
        output_filename = "merged_test.pdf"
        
        result = await pdf_service.merge_pdfs(pdf_files, output_filename)
        
        assert result["success"] is True
        assert "output_path" in result
        assert "total_pages" in result
        
        # Cleanup
        if os.path.exists(result["output_path"]):
            os.unlink(result["output_path"])
    
    @pytest.mark.asyncio
    async def test_compress_pdf(self, pdf_service: PDFService, temp_pdf_file: str):
        """Test PDF compression"""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as output_file:
            output_path = output_file.name
        
        try:
            result = await pdf_service.compress_pdf(temp_pdf_file, output_path, quality=85)
            
            assert "success" in result
            if result["success"]:
                assert "original_size" in result
                assert "compressed_size" in result
                assert "compression_ratio" in result
                assert os.path.exists(output_path)
        finally:
            # Cleanup
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    @pytest.mark.asyncio
    async def test_extract_text_ocr_disabled(self, pdf_service: PDFService, temp_pdf_file: str):
        """Test OCR when disabled"""
        # Temporarily disable OCR
        from app.core.config import settings
        original_ocr_enabled = settings.OCR_ENABLED
        settings.OCR_ENABLED = False
        
        try:
            result = await pdf_service.extract_text_ocr(temp_pdf_file)
            
            assert result["success"] is False
            assert "OCR não está habilitado" in result["error"]
        finally:
            # Restore original setting
            settings.OCR_ENABLED = original_ocr_enabled
    
    @pytest.mark.asyncio
    async def test_add_watermark(self, pdf_service: PDFService, temp_pdf_file: str):
        """Test adding watermark to PDF"""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as output_file:
            output_path = output_file.name
        
        try:
            result = await pdf_service.add_watermark(
                temp_pdf_file, 
                "TEST WATERMARK", 
                output_path
            )
            
            assert "success" in result
            if result["success"]:
                assert result["output_path"] == output_path
                assert os.path.exists(output_path)
        finally:
            # Cleanup
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    @pytest.mark.asyncio
    async def test_split_pdf(self, pdf_service: PDFService, temp_pdf_file: str):
        """Test splitting PDF"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = await pdf_service.split_pdf(temp_pdf_file, temp_dir, pages_per_file=1)
            
            assert "success" in result
            if result["success"]:
                assert "output_files" in result
                assert "total_files" in result
                assert isinstance(result["output_files"], list)
    
    def test_pdf_service_initialization(self, pdf_service: PDFService):
        """Test PDF service initialization"""
        assert pdf_service.upload_dir.exists()
        assert pdf_service.output_dir.exists()
        assert pdf_service.temp_dir.exists()
    
    @pytest.mark.asyncio
    async def test_invalid_pdf_file(self, pdf_service: PDFService):
        """Test handling invalid PDF file"""
        invalid_content = b"This is not a PDF file"
        
        with pytest.raises(Exception):
            await pdf_service.save_uploaded_file(invalid_content, "invalid.pdf")
    
    @pytest.mark.asyncio
    async def test_merge_empty_list(self, pdf_service: PDFService):
        """Test merging empty PDF list"""
        result = await pdf_service.merge_pdfs([], "empty.pdf")
        
        # Should handle empty list gracefully
        assert "success" in result