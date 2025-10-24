import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from main import app
from services.memory_service import ConversationMemory

@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def sample_session_id():
    """Sample session ID for testing"""
    return "test-session-123"


@pytest.fixture
def memory_service():
    """Memory service instance"""
    return ConversationMemory(data_file="data/test_conversations.json")


@pytest.fixture
def sample_appointment():
    """Sample appointment data"""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "service": "Teeth Cleaning",
        "date": "2024-12-25",
        "time": "14:00",
        "dentist": "Dr. Emily Chen"
    }


@pytest.fixture
def cleanup_test_files():
    """Cleanup test files after tests"""
    yield
    # Cleanup
    test_files = [
        Path("data/test_conversations.json"),
        Path("backend/uploads/test_*.wav"),
        Path("backend/audio_outputs/test_*.mp3")
    ]
    for pattern in test_files:
        if pattern.exists():
            pattern.unlink()