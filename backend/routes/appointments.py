from fastapi import APIRouter, HTTPException
from services.memory_service import ConversationMemory

router = APIRouter()
memory = ConversationMemory()

@router.get("/list")
async def list_appointments():
    """Get all appointments"""
    all_appointments = []
    for session_id, session_data in memory.sessions.items():
        for appointment in session_data.get("appointments", []):
            all_appointments.append({
                "session_id": session_id,
                **appointment
            })
    return {"appointments": all_appointments, "count": len(all_appointments)}

@router.get("/{session_id}")
async def get_session_appointments(session_id: str):
    """Get appointments for a specific session"""
    if session_id not in memory.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "appointments": memory.sessions[session_id].get("appointments", [])
    }