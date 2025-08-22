import pytest
import os
from fastapi.testclient import TestClient
from app.models.user import User
from app.models.pdf_project import PDFProject

class TestPDFOperations:
    """Test PDF operations endpoints"""
    
    def test_create_project(self, client: TestClient, auth_headers: dict):
        """Test creating a new PDF project"""
        project_data = {
            "name": "Test Project",
            "description": "A test project for PDF operations",
            "is_public": False
        }
        
        response = client.post("/api/pdf/projects/", json=project_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == project_data["name"]
        assert data["description"] == project_data["description"]
        assert data["is_public"] == project_data["is_public"]
        assert data["status"] == "draft"
    
    def test_list_projects(self, client: TestClient, auth_headers: dict, test_project: PDFProject):
        """Test listing user projects"""
        response = client.get("/api/pdf/projects/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(project["id"] == test_project.id for project in data)
    
    def test_get_project(self, client: TestClient, auth_headers: dict, test_project: PDFProject):
        """Test getting a specific project"""
        response = client.get(f"/api/pdf/projects/{test_project.id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_project.id
        assert data["name"] == test_project.name
    
    def test_get_nonexistent_project(self, client: TestClient, auth_headers: dict):
        """Test getting a non-existent project"""
        response = client.get("/api/pdf/projects/99999", headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_upload_pdf_files(self, client: TestClient, auth_headers: dict, test_project: PDFProject, temp_pdf_file: str):
        """Test uploading PDF files to a project"""
        with open(temp_pdf_file, "rb") as f:
            files = {"files": ("test.pdf", f, "application/pdf")}
            response = client.post(
                f"/api/pdf/projects/{test_project.id}/upload",
                files=files,
                headers=auth_headers
            )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["original_filename"] == "test.pdf"
        assert data[0]["project_id"] == test_project.id
    
    def test_upload_invalid_file(self, client: TestClient, auth_headers: dict, test_project: PDFProject):
        """Test uploading non-PDF file"""
        files = {"files": ("test.txt", b"Not a PDF", "text/plain")}
        response = client.post(
            f"/api/pdf/projects/{test_project.id}/upload",
            files=files,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert "não é um PDF válido" in response.json()["detail"]
    
    def test_reorder_files(self, client: TestClient, auth_headers: dict, test_project: PDFProject):
        """Test reordering files in a project"""
        # First upload some files
        with open(temp_pdf_file, "rb") as f:
            files = [("files", ("test1.pdf", f, "application/pdf")),
                    ("files", ("test2.pdf", f, "application/pdf"))]
            client.post(
                f"/api/pdf/projects/{test_project.id}/upload",
                files=files,
                headers=auth_headers
            )
        
        # Then reorder them
        reorder_data = [
            {"file_id": 1, "order_index": 1},
            {"file_id": 2, "order_index": 0}
        ]
        
        response = client.put(
            f"/api/pdf/projects/{test_project.id}/reorder",
            json=reorder_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert "Ordem dos arquivos atualizada" in response.json()["message"]
    
    def test_merge_project_pdfs(self, client: TestClient, auth_headers: dict, test_project: PDFProject, temp_pdf_file: str):
        """Test merging PDFs in a project"""
        # First upload a file
        with open(temp_pdf_file, "rb") as f:
            files = {"files": ("test.pdf", f, "application/pdf")}
            client.post(
                f"/api/pdf/projects/{test_project.id}/upload",
                files=files,
                headers=auth_headers
            )
        
        # Then merge
        merge_data = {"output_filename": "merged_test.pdf"}
        response = client.post(
            f"/api/pdf/projects/{test_project.id}/merge",
            json=merge_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "PDFs mesclados com sucesso" in data["message"]
        assert "operation_id" in data
    
    def test_merge_empty_project(self, client: TestClient, auth_headers: dict, test_project: PDFProject):
        """Test merging an empty project"""
        merge_data = {"output_filename": "empty_merge.pdf"}
        response = client.post(
            f"/api/pdf/projects/{test_project.id}/merge",
            json=merge_data,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert "Nenhum arquivo PDF encontrado" in response.json()["detail"]
    
    def test_download_project_output(self, client: TestClient, auth_headers: dict, test_project: PDFProject):
        """Test downloading project output"""
        # This test assumes the project has been processed
        response = client.get(
            f"/api/pdf/projects/{test_project.id}/download",
            headers=auth_headers
        )
        
        # Should return 404 since no output file exists
        assert response.status_code == 404
    
    def test_list_operations(self, client: TestClient, auth_headers: dict):
        """Test listing PDF operations"""
        response = client.get("/api/pdf/operations/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_unauthorized_access(self, client: TestClient, test_project: PDFProject):
        """Test accessing endpoints without authentication"""
        response = client.get("/api/pdf/projects/")
        assert response.status_code == 401
        
        response = client.get(f"/api/pdf/projects/{test_project.id}")
        assert response.status_code == 401
        
        response = client.post("/api/pdf/projects/", json={"name": "Test"})
        assert response.status_code == 401