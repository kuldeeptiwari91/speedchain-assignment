import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import io

class TestIntegration:
    """Integration tests for complete workflows"""
    
    def test_complete_conversation_flow(self, client):
        # 1. Get greeting
        response = client.post("/api/conversation/greeting")
        assert response.status_code == 200
        session_id = response.json()["session_id"]
        
        # 2. Get conversation history
        response = client.get(f"/api/conversation/history/{session_id}")
        assert response.status_code == 200
        assert len(response.json()["messages"]) == 1  # Greeting message
    
    def test_appointment_workflow(self, client, sample_appointment):
        # This would test the complete appointment booking flow
        # In a real scenario, you'd simulate audio upload and processing
        pass