from gtts import gTTS
from pathlib import Path
import hashlib
import os

class TTSService:
    """Text-to-Speech Service using gTTS (Google TTS - Free)"""
    
    def __init__(self):
        # Get the directory where this file is located
        current_dir = Path(__file__).parent.parent
        self.OUTPUT_DIR = current_dir / "audio_outputs"
        self.OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    
    async def text_to_speech(self, text: str) -> str:
        """Convert text to speech"""
        try:
            # Create unique filename based on text hash
            text_hash = hashlib.md5(text.encode()).hexdigest()[:10]
            output_path = self.OUTPUT_DIR / f"response_{text_hash}.mp3"
            
            # Check if already exists (cache)
            if output_path.exists():
                return str(output_path)
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(output_path))
            
            return str(output_path)
            
        except Exception as e:
            raise Exception(f"TTS Error: {str(e)}")