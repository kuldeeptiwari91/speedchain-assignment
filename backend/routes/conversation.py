from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from services.stt_service import STTService
from services.llm_service import LLMService
from services.tts_service import TTSService
from services.memory_service import ConversationMemory
from services.email_service import EmailService
import aiofiles
import os
from pathlib import Path
import uuid
import traceback

router = APIRouter()

# Initialize services
stt_service = STTService()
llm_service = LLMService()
tts_service = TTSService()
memory = ConversationMemory()
email_service = EmailService()

# Paths
BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
AUDIO_OUTPUT_DIR = BASE_DIR / "audio_outputs"

# Create directories
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
AUDIO_OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

print(f"[Routes] Base directory: {BASE_DIR}")
print(f"[Routes] Upload directory: {UPLOAD_DIR}")
print(f"[Routes] Audio output directory: {AUDIO_OUTPUT_DIR}")

@router.post("/process-voice")
async def process_voice(audio: UploadFile = File(...), session_id: str = None):
    """Process voice input: STT -> LLM -> TTS"""
    try:
        print(f"\n[Process] New voice message")
        
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        print(f"[Process] Session ID: {session_id}")
        
        # Save uploaded audio
        audio_path = UPLOAD_DIR / f"{session_id}_{audio.filename}"
        async with aiofiles.open(audio_path, 'wb') as f:
            content = await audio.read()
            await f.write(content)
        
        print(f"[Process] Saved audio to: {audio_path}")
        
        # Step 1: Speech to Text
        print(f"[Process] Starting STT...")
        user_text = await stt_service.transcribe_audio(str(audio_path))
        print(f"[Process] User said: {user_text}")
        
        # Add user message to memory
        memory.add_message(session_id, "user", user_text)
        
        # Step 2: Get LLM response
        print(f"[Process] Getting LLM response...")
        conversation_history = memory.get_history(session_id)
        llm_result = await llm_service.get_response(user_text, conversation_history)
        
        assistant_response = llm_result["response"]
        intent = llm_result["intent"]
        metadata = llm_result.get("metadata")
        
        print(f"[Process] Assistant: {assistant_response}")
        print(f"[Process] Intent: {intent}")
        
        # Add assistant message to memory
        memory.add_message(session_id, "assistant", assistant_response)
        
        # Step 3: Handle appointment booking
        if intent == "book_appointment" and metadata:
            print(f"[Process] Booking appointment: {metadata}")
            memory.update_metadata(session_id, metadata)
            memory.add_appointment(session_id, metadata)
            
            # Send confirmation email
            if "email" in metadata:
                await email_service.send_appointment_confirmation(
                    metadata["email"],
                    metadata
                )
        
        # Step 4: Text to Speech
        print(f"[Process] Generating TTS...")
        audio_response_path = await tts_service.text_to_speech(assistant_response)
        print(f"[Process] Audio generated at: {audio_response_path}")
        
        # Verify audio file exists
        if not Path(audio_response_path).exists():
            raise Exception(f"Audio file not generated: {audio_response_path}")
        
        # Cleanup uploaded file
        try:
            os.remove(audio_path)
            print(f"[Process] Cleaned up uploaded file")
        except:
            pass
        
        audio_filename = Path(audio_response_path).name
        
        return {
            "session_id": session_id,
            "user_text": user_text,
            "assistant_text": assistant_response,
            "intent": intent,
            "metadata": metadata,
            "audio_url": f"/api/conversation/audio/{audio_filename}"
        }
        
    except Exception as e:
        print(f"[Process] ✗ Error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/audio/{filename}")
async def get_audio(filename: str):
    """Serve audio file"""
    try:
        print(f"\n[Audio] Request for file: {filename}")
        
        audio_path = AUDIO_OUTPUT_DIR / filename
        
        print(f"[Audio] Full path: {audio_path}")
        print(f"[Audio] File exists: {audio_path.exists()}")
        
        if not audio_path.exists():
            # List all files in directory for debugging
            all_files = list(AUDIO_OUTPUT_DIR.glob("*"))
            print(f"[Audio] Files in directory: {[f.name for f in all_files]}")
            
            raise HTTPException(
                status_code=404, 
                detail=f"Audio file not found: {filename}"
            )
        
        file_size = audio_path.stat().st_size
        print(f"[Audio] Serving file. Size: {file_size} bytes")
        
        return FileResponse(
            path=str(audio_path),
            media_type="audio/mpeg",
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Audio] ✗ Error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_conversation_history(session_id: str):
    """Get conversation history"""
    print(f"\n[History] Request for session: {session_id}")
    
    if session_id not in memory.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return memory.sessions[session_id]

@router.get("/greeting")  # Changed to GET
async def get_greeting(session_id: str = None):
    """Get initial greeting"""
    try:
        print(f"\n[Greeting] New greeting request")
        
        if not session_id:
            session_id = str(uuid.uuid4())
        
        print(f"[Greeting] Session ID: {session_id}")
        
        greeting_text = "Hello! I'm Sarah, the AI receptionist at SmileCare Dental. How may I help you today?"
        
        memory.create_session(session_id)
        memory.add_message(session_id, "assistant", greeting_text)
        
        # Generate greeting audio
        print(f"[Greeting] Calling TTS service...")
        audio_path = await tts_service.text_to_speech(greeting_text)
        print(f"[Greeting] TTS returned path: {audio_path}")
        
        # Convert to Path object and verify
        audio_file = Path(audio_path)
        print(f"[Greeting] Audio file exists: {audio_file.exists()}")
        
        if not audio_file.exists():
            raise Exception(f"Audio file not found at: {audio_path}")
        
        audio_filename = audio_file.name
        audio_url = f"/api/conversation/audio/{audio_filename}"
        
        print(f"[Greeting] Audio filename: {audio_filename}")
        print(f"[Greeting] Audio URL: {audio_url}")
        
        response = {
            "session_id": session_id,
            "text": greeting_text,
            "audio_url": audio_url
        }
        
        print(f"[Greeting] Returning response: {response}")
        
        return response
        
    except Exception as e:
        print(f"[Greeting] ✗ Error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))