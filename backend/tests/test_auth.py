import pytest
from fastapi.testclient import TestClient
from app.models.user import User

class TestAuth:
    """Test authentication endpoints"""
    
    def test_register_user(self, client: TestClient):
        """Test user registration"""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "full_name": "New User",
            "password": "newpassword123"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert "hashed_password" not in data
    
    def test_register_duplicate_user(self, client: TestClient, test_user: User):
        """Test registration with duplicate username"""
        user_data = {
            "username": test_user.username,
            "email": "different@example.com",
            "password": "password123"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 400
        assert "já cadastrado" in response.json()["detail"]
    
    def test_login_valid_user(self, client: TestClient, test_user: User):
        """Test login with valid credentials"""
        login_data = {
            "username": test_user.username,
            "password": "testpassword123"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == test_user.username
    
    def test_login_invalid_credentials(self, client: TestClient, test_user: User):
        """Test login with invalid credentials"""
        login_data = {
            "username": test_user.username,
            "password": "wrongpassword"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == 401
        assert "Credenciais inválidas" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with non-existent user"""
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == 401
    
    def test_refresh_token(self, client: TestClient, auth_headers: dict):
        """Test token refresh"""
        response = client.post("/api/auth/refresh", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_refresh_token_invalid(self, client: TestClient):
        """Test token refresh with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/api/auth/refresh", headers=headers)
        
        assert response.status_code == 401
    
    def test_logout(self, client: TestClient, auth_headers: dict):
        """Test logout"""
        response = client.post("/api/auth/logout", headers=auth_headers)
        
        assert response.status_code == 200
        assert "Logout realizado" in response.json()["message"]
    
    def test_register_invalid_email(self, client: TestClient):
        """Test registration with invalid email"""
        user_data = {
            "username": "testuser2",
            "email": "invalid-email",
            "password": "password123"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 422
    
    def test_register_short_password(self, client: TestClient):
        """Test registration with short password"""
        user_data = {
            "username": "testuser3",
            "email": "test3@example.com",
            "password": "123"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 422