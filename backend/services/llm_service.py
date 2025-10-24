import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"[LLM Init] API Key loaded: {GEMINI_API_KEY[:10] if GEMINI_API_KEY else 'NOT FOUND'}...")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

genai.configure(api_key=GEMINI_API_KEY)
print(f"[LLM Init] ✓ Gemini configured successfully")

class LLMService:
    """Language Model Service using Google Gemini 2.5"""
    
    SYSTEM_INSTRUCTION = """You are Sarah, a friendly and professional AI receptionist at SmileCare Dental Clinic.

About SmileCare Dental:
- Services: General Checkup, Teeth Cleaning, Root Canal, Teeth Whitening, Braces Consultation, Dental Implants
- Dentists:
  * Dr. Emily Chen - General Dentistry, Teeth Cleaning
  * Dr. James Wilson - Root Canal Specialist
  * Dr. Priya Sharma - Cosmetic Dentistry, Whitening
  * Dr. Mark Johnson - Orthodontics, Braces
- Working Hours: Monday to Saturday, 9 AM to 6 PM
- Location: 123 Healthcare Ave, Downtown

Your responsibilities:
1. Greet patients warmly
2. Ask for their name if not provided
3. Understand what service they need
4. Ask for preferred date and time
5. Ask for preferred dentist (or suggest based on service)
6. Collect their email for confirmation
7. Confirm all details before booking

Be conversational, empathetic, and helpful. Keep responses concise (2-3 sentences max) and natural.

IMPORTANT: When you have collected ALL required information (name, service, date, time, email), include this marker:
APPOINTMENT_READY
name: [patient name]
email: [patient email]
service: [service type]
date: [YYYY-MM-DD]
time: [HH:MM]
dentist: [dentist name]
END_APPOINTMENT

Example:
"Perfect John! I'll book your teeth cleaning for December 25, 2024 at 2:00 PM with Dr. Emily Chen.

APPOINTMENT_READY
name: John
email: john@example.com
service: Teeth Cleaning
date: 2024-12-25
time: 14:00
dentist: Dr. Emily Chen
END_APPOINTMENT"
"""

    def __init__(self):
        try:
            # Use Gemini 2.5 Flash with system instruction
            self.model = genai.GenerativeModel(
                'gemini-2.5-flash',
                system_instruction=self.SYSTEM_INSTRUCTION
            )
            print(f"[LLM] ✓ Gemini 2.5 Flash initialized")
        except Exception as e:
            print(f"[LLM] ✗ Failed to initialize: {e}")
            raise
        
    async def get_response(self, user_message: str, conversation_history: List[Dict[str, str]]) -> Dict:
        """Get AI response using Gemini"""
        try:
            print(f"[LLM] User message: '{user_message}'")
            
            # Build conversation context
            context = ""
            if conversation_history:
                context = "Previous conversation:\n"
                for msg in conversation_history[-6:]:  # Last 6 messages
                    role = "Patient" if msg["role"] == "user" else "Sarah"
                    context += f"{role}: {msg['content']}\n"
                context += "\n"
            
            full_prompt = context + f"Patient: {user_message}\nSarah:"
            
            print(f"[LLM] Sending request to Gemini...")
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=250,
                )
            )
            
            # Extract text (debug showed response.text works)
            assistant_message = response.text
            
            if not assistant_message:
                raise Exception("Empty response from Gemini")
            
            print(f"[LLM] ✓ Response ({len(assistant_message)} chars): '{assistant_message[:100]}...'")
            
            # Parse intent and metadata
            intent = "conversation"
            metadata = None
            
            if "APPOINTMENT_READY" in assistant_message and "END_APPOINTMENT" in assistant_message:
                print(f"[LLM] Detected appointment booking")
                intent = "book_appointment"
                
                start_idx = assistant_message.find("APPOINTMENT_READY")
                end_idx = assistant_message.find("END_APPOINTMENT")
                
                appointment_block = assistant_message[start_idx:end_idx]
                
                # Parse metadata
                metadata = {}
                for line in appointment_block.split('\n'):
                    if ':' in line and 'APPOINTMENT_READY' not in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip().lower()] = value.strip()
                
                print(f"[LLM] Extracted metadata: {metadata}")
                
                # Remove marker from response
                assistant_message = assistant_message[:start_idx].strip()
            
            return {
                "response": assistant_message,
                "intent": intent,
                "metadata": metadata
            }
            
        except Exception as e:
            print(f"[LLM] ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "response": "I'm having technical difficulties. Could you please repeat that?",
                "intent": "error",
                "metadata": None
            }