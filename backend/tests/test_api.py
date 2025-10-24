import pytest
from fastapi.testclient import TestClient

class TestAPIEndpoints:
    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "AI Receptionist" in response.json()["message"]
    
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_greeting_endpoint(self, client):
        response = client.post("/api/conversation/greeting")
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert "text" in data
        assert "audio_url" in data
    
    def test_appointments_list(self, client):
        response = client.get("/api/appointments/list")
        assert response.status_code == 200
        assert "appointments" in response.json()