import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv
from datetime import datetime, timedelta
from textwrap import dedent
import os

load_dotenv(override=True)

# Load API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"[LLM Init] API Key loaded: {GEMINI_API_KEY[:10] if GEMINI_API_KEY else 'NOT FOUND'}...")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
print("[LLM Init] ✓ Gemini configured successfully")


class LLMService:
    """Language Model Service using Google Gemini 2.5 Flash"""

    def __init__(self):
        # Build dynamic system instruction with date awareness
        self.SYSTEM_INSTRUCTION = self._build_system_instruction()

        try:
            self.model = genai.GenerativeModel(
                "gemini-2.5-flash",
                system_instruction=self.SYSTEM_INSTRUCTION
            )
            print("[LLM] ✓ Gemini 2.5 Flash initialized successfully")
        except Exception as e:
            print(f"[LLM] ✗ Failed to initialize: {e}")
            raise

    def _build_system_instruction(self) -> str:
        """Build dynamic system prompt with current date context"""
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)

        return dedent(f"""
            You are Sarah, a friendly and professional AI receptionist at SmileCare Dental Clinic.

            TODAY'S DATE: {today.strftime('%A, %B %d, %Y')}

            About SmileCare Dental:
            - Services: General Checkup, Teeth Cleaning, Root Canal, Teeth Whitening, Braces Consultation, Dental Implants
            - Dentists:
              * Dr. Emily Chen - General Dentistry, Teeth Cleaning
              * Dr. James Wilson - Root Canal Specialist
              * Dr. Priya Sharma - Cosmetic Dentistry, Whitening
              * Dr. Mark Johnson - Orthodontics, Braces
            - Working Hours: Monday to Saturday, 9 AM to 6 PM (Closed Sundays)
            - Location: 123 Healthcare Ave, Downtown

            Your responsibilities:
            1. Greet patients warmly
            2. Ask for their name if not provided
            3. Understand what service they need
            4. Suggest available dates within the next 7-14 days (e.g., "tomorrow", "this Friday", or "next Monday")
            5. Ask for a preferred time (suggest 9 AM, 10 AM, 11 AM, 2 PM, 3 PM, 4 PM, or 5 PM)
            6. Suggest an appropriate dentist based on the service
            7. Collect their email for confirmation
            8. Confirm all details clearly and naturally

            Guidelines:
            - Suggest only valid business days (Mon-Sat)
            - When user says "tomorrow" → {tomorrow.strftime('%B %d, %Y')}
            - When user says "next week" → suggest specific days between {next_week.strftime('%B %d')} and {(next_week + timedelta(days=6)).strftime('%B %d')}
            - Be conversational, empathetic, and concise (max 3-4 sentences)
            - Complete all sentences fully

            When you have ALL required info (name, service, date, time, email), include this hidden marker at the END:

            APPOINTMENT_READY
            name: [patient name]
            email: [patient email]
            service: [service type]
            date: [YYYY-MM-DD format]
            time: [HH:MM in 24-hour format]
            dentist: [dentist name]
            END_APPOINTMENT

            This marker will not be shown to users, so write your response naturally above it.

            Example:
            "Perfect, John! I've scheduled your teeth whitening for tomorrow at 11 AM with Dr. Priya Sharma. You'll receive a confirmation email at john@email.com shortly. Looking forward to seeing you!

            APPOINTMENT_READY
            name: John
            email: john@email.com
            service: Teeth Whitening
            date: {tomorrow.strftime('%Y-%m-%d')}
            time: 11:00
            dentist: Dr. Priya Sharma
            END_APPOINTMENT"
        """).strip()

    async def get_response(self, user_message: str, conversation_history: List[Dict[str, str]]) -> Dict:
        """Get AI response using Gemini with conversation context"""
        try:
            print(f"[LLM] User message: '{user_message}'")

            # Build conversation context (last 6 messages)
            context = ""
            if conversation_history:
                context = "Previous conversation:\n"
                for msg in conversation_history[-6:]:
                    role = "Patient" if msg["role"] == "user" else "Sarah"
                    context += f"{role}: {msg['content']}\n"
                context += "\n"

            # Build prompt (system instruction is already set in model)
            full_prompt = f"{context}Patient: {user_message}\nSarah:"

            print("[LLM] Sending request to Gemini...")
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.95,
                    max_output_tokens=400,
                ),
            )

            assistant_message = (response.text or "").strip()
            if not assistant_message:
                raise Exception("Empty response from Gemini")

            print(f"[LLM] ✓ Raw response ({len(assistant_message)} chars)")

            # Default values
            intent = "conversation"
            metadata = None

            # Check for appointment booking
            if "APPOINTMENT_READY" in assistant_message and "END_APPOINTMENT" in assistant_message:
                print("[LLM] 📅 Appointment booking detected")
                intent = "book_appointment"

                # Extract appointment block
                start_idx = assistant_message.find("APPOINTMENT_READY")
                end_idx = assistant_message.find("END_APPOINTMENT") + len("END_APPOINTMENT")
                appointment_block = assistant_message[start_idx:end_idx]

                # Parse metadata
                metadata = {}
                try:
                    for line in appointment_block.splitlines():
                        line = line.strip()
                        if ":" in line and "APPOINTMENT" not in line:
                            parts = line.split(":", 1)
                            if len(parts) == 2:
                                key, value = parts
                                metadata[key.strip().lower()] = value.strip()
                except Exception as parse_error:
                    print(f"[LLM] ⚠️ Metadata parsing error: {parse_error}")
                    metadata = None

                # Validate required fields
                required_fields = ["name", "email", "service", "date", "time", "dentist"]
                if metadata and all(field in metadata for field in required_fields):
                    print(f"[LLM] ✓ Extracted metadata: {metadata}")
                else:
                    missing = [f for f in required_fields if f not in (metadata or {})]
                    print(f"[LLM] ⚠️ Incomplete metadata. Missing: {missing}")
                    intent = "conversation"
                    metadata = None

                # Remove marker from response
                assistant_message = assistant_message[:start_idx].strip()

            # Safety cleanup - remove any stray markers
            if "APPOINTMENT_READY" in assistant_message or "END_APPOINTMENT" in assistant_message:
                assistant_message = assistant_message.split("APPOINTMENT_READY")[0].strip()
                print("[LLM] Cleanup: Removed stray appointment markers")

            return {
                "response": assistant_message,
                "intent": intent,
                "metadata": metadata,
            }

        except Exception as e:
            print(f"[LLM] ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "response": "I'm having technical difficulties. Could you please repeat that?",
                "intent": "error",
                "metadata": None,
            }