import speech_recognition as sr
from pathlib import Path
from pydub import AudioSegment
import os

class STTService:
    """Speech-to-Text Service using Google's free API"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Adjust recognition settings for better accuracy
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio file to text"""
        try:
            audio_path = Path(audio_file_path)
            
            print(f"[STT] Processing audio file: {audio_path}")
            print(f"[STT] File exists: {audio_path.exists()}")
            print(f"[STT] File size: {audio_path.stat().st_size} bytes")
            
            # Check if file is empty
            if audio_path.stat().st_size == 0:
                raise Exception("Audio file is empty")
            
            # Convert audio to proper WAV format
            converted_path = self._convert_to_wav(str(audio_path))
            
            print(f"[STT] Converted audio path: {converted_path}")
            print(f"[STT] Starting transcription...")
            
            # Transcribe
            with sr.AudioFile(converted_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record the audio
                audio_data = self.recognizer.record(source)
                
                # Transcribe using Google
                print(f"[STT] Calling Google Speech Recognition API...")
                text = self.recognizer.recognize_google(audio_data)
                
                print(f"[STT] ✓ Transcription successful: '{text}'")
                
                # Clean up converted file if it's different from original
                if converted_path != str(audio_path):
                    try:
                        os.remove(converted_path)
                    except:
                        pass
                
                return text
                
        except sr.UnknownValueError:
            raise Exception("Could not understand audio. Please speak clearly and ensure your microphone is working.")
        except sr.RequestError as e:
            raise Exception(f"Could not request results from speech recognition service: {e}")
        except Exception as e:
            raise Exception(f"STT Error: {str(e)}")
    
    def _convert_to_wav(self, audio_file_path: str) -> str:
        """Convert audio to WAV format with correct parameters"""
        try:
            audio_path = Path(audio_file_path)
            
            # If already a WAV file, try to use it directly
            # but re-encode to ensure correct format
            output_path = audio_path.parent / f"{audio_path.stem}_converted.wav"
            
            print(f"[STT] Converting audio to proper WAV format...")
            
            # Load audio file (supports many formats)
            audio = AudioSegment.from_file(str(audio_path))
            
            # Convert to WAV with specific parameters that work with speech_recognition
            audio = audio.set_frame_rate(16000)  # 16kHz sample rate
            audio = audio.set_channels(1)         # Mono
            audio = audio.set_sample_width(2)     # 16-bit
            
            # Export as WAV
            audio.export(
                str(output_path),
                format="wav",
                parameters=["-ar", "16000", "-ac", "1"]
            )
            
            print(f"[STT] Audio converted successfully")
            print(f"[STT] Original size: {audio_path.stat().st_size} bytes")
            print(f"[STT] Converted size: {output_path.stat().st_size} bytes")
            
            return str(output_path)
            
        except Exception as e:
            print(f"[STT] Warning: Could not convert audio: {e}")
            # If conversion fails, try to use original file
            return audio_file_path