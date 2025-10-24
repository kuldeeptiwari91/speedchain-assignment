import json
from typing import List, Dict
from pathlib import Path
from datetime import datetime

class ConversationMemory:
    """Manages conversation history and metadata"""
    
    def __init__(self, data_file: str = None):
        if data_file is None:
            # Get path relative to backend directory
            backend_dir = Path(__file__).parent.parent
            data_dir = backend_dir.parent / "data"
            data_dir.mkdir(exist_ok=True, parents=True)
            self.data_file = data_dir / "conversations.json"
        else:
            self.data_file = Path(data_file)
            self.data_file.parent.mkdir(exist_ok=True, parents=True)
        
        self.sessions = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load conversation data from file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_data(self):
        """Save conversation data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)
    
    def create_session(self, session_id: str) -> None:
        """Create a new conversation session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "created_at": datetime.now().isoformat(),
                "messages": [],
                "metadata": {},
                "appointments": []
            }
            self._save_data()
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add message to session history"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        self.sessions[session_id]["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self._save_data()
    
    def get_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for session"""
        if session_id not in self.sessions:
            return []
        
        # Return in format for LLM
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.sessions[session_id]["messages"]
        ]
    
    def update_metadata(self, session_id: str, metadata: Dict):
        """Update session metadata"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        self.sessions[session_id]["metadata"].update(metadata)
        self._save_data()
    
    def add_appointment(self, session_id: str, appointment: Dict):
        """Add appointment to session"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        appointment["booked_at"] = datetime.now().isoformat()
        self.sessions[session_id]["appointments"].append(appointment)
        self._save_data()