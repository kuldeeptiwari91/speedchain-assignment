import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Gemini API with gemini-2.5-flash...\n")

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("✗ ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)

print(f"✓ API Key found (length: {len(api_key)})")

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    print("✓ Gemini configured")
except Exception as e:
    print(f"✗ Configuration error: {e}")
    exit(1)

# Test with gemini-2.5-flash
try:
    print("\nTesting model: gemini-2.5-flash")
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    response = model.generate_content(
        "You are a dental receptionist. Greet a patient who just walked in.",
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=100,
        )
    )
    
    print(f"✓ Model works!")
    
    # Handle different response structures
    try:
        # Try simple text accessor first
        response_text = response.text
    except:
        # Fall back to parts accessor
        response_text = ""
        for part in response.parts:
            response_text += part.text
    
    print(f"\nResponse:\n{response_text}")
    print("\n✓✓✓ Gemini 2.5 Flash is working correctly! ✓✓✓")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()