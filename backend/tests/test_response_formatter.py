import pytest
from utils.response_formatter import (
    format_appointment_response,
    format_error_response,
    format_conversation_summary
)

class TestResponseFormatter:
    def test_format_appointment(self, sample_appointment):
        response = format_appointment_response(sample_appointment)
        
        assert response["success"] == True
        assert response["appointment"]["patient_name"] == "John Doe"
        assert "id" in response["appointment"]
    
    def test_format_error(self):
        response = format_error_response("Test error", "Details here")
        
        assert response["success"] == False
        assert response["error"] == "Test error"
        assert response["details"] == "Details here"
    
    def test_format_summary(self):
        session_data = {
            "session_id": "test-123",
            "created_at": "2024-01-01T00:00:00",
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi"}
            ],
            "metadata": {"name": "John"},
            "appointments": []
        }
        
        summary = format_conversation_summary(session_data)
        
        assert summary["total_messages"] == 2
        assert summary["user_messages"] == 1
        assert summary["assistant_messages"] == 1