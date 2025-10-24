from dotenv import load_dotenv
import os

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

if gemini_key:
    print(f"✓ GEMINI_API_KEY found")
    print(f"  Length: {len(gemini_key)}")
    print(f"  Starts with: {gemini_key[:10]}...")
    print(f"  Ends with: ...{gemini_key[-5:]}")
else:
    print("✗ GEMINI_API_KEY not found!")
    print("\nCreate a .env file in the backend folder with:")
    print("GEMINI_API_KEY=your_key_here")