import pytest
from services.memory_service import ConversationMemory
import json
from pathlib import Path

class TestMemoryService:
    def test_create_session(self, memory_service, sample_session_id):
        memory_service.create_session(sample_session_id)
        assert sample_session_id in memory_service.sessions
        assert memory_service.sessions[sample_session_id]["messages"] == []
    
    def test_add_message(self, memory_service, sample_session_id):
        memory_service.create_session(sample_session_id)
        memory_service.add_message(sample_session_id, "user", "Hello")
        
        history = memory_service.get_history(sample_session_id)
        assert len(history) == 1
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Hello"
    
    def test_update_metadata(self, memory_service, sample_session_id):
        memory_service.create_session(sample_session_id)
        metadata = {"name": "John", "email": "john@example.com"}
        memory_service.update_metadata(sample_session_id, metadata)
        
        assert memory_service.sessions[sample_session_id]["metadata"] == metadata
    
    def test_add_appointment(self, memory_service, sample_session_id, sample_appointment):
        memory_service.create_session(sample_session_id)
        memory_service.add_appointment(sample_session_id, sample_appointment)
        
        appointments = memory_service.sessions[sample_session_id]["appointments"]
        assert len(appointments) == 1
        assert appointments[0]["name"] == "John Doe"
    
    def test_persistence(self, sample_session_id):
        # Create and save
        memory1 = ConversationMemory(data_file="data/test_persistence.json")
        memory1.create_session(sample_session_id)
        memory1.add_message(sample_session_id, "user", "Test message")
        
        # Load in new instance
        memory2 = ConversationMemory(data_file="data/test_persistence.json")
        history = memory2.get_history(sample_session_id)
        
        assert len(history) == 1
        assert history[0]["content"] == "Test message"
        
        # Cleanup
        Path("data/test_persistence.json").unlink()