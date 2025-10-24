import asyncio
from services.email_service import EmailService
from dotenv import load_dotenv
import os

load_dotenv()

async def test_email():
    print("="*60)
    print("EMAIL SERVICE TEST")
    print("="*60)
    
    # Check environment variables
    print("\n[1] Checking environment variables...")
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = os.getenv("SMTP_PORT", "587")
    
    print(f"    SMTP_EMAIL: {smtp_email if smtp_email else '✗ NOT SET'}")
    print(f"    SMTP_PASSWORD: {'✓ SET' if smtp_password else '✗ NOT SET'}")
    print(f"    SMTP_SERVER: {smtp_server}")
    print(f"    SMTP_PORT: {smtp_port}")
    
    if not smtp_email or not smtp_password:
        print("\n✗ Email credentials not configured!")
        print("\nTo fix:")
        print("1. Add to backend/.env file:")
        print("   SMTP_EMAIL=your_email@gmail.com")
        print("   SMTP_PASSWORD=your_app_password")
        print("\n2. Get App Password from: https://myaccount.google.com/apppasswords")
        return
    
    # Initialize email service
    print("\n[2] Initializing email service...")
    email_service = EmailService()
    
    # Test appointment data
    test_appointment = {
        "name": "Test User",
        "email": input("\nEnter YOUR email to test: ").strip(),
        "service": "Teeth Cleaning",
        "date": "2025-01-25",
        "time": "10:00",
        "dentist": "Dr. Emily Chen"
    }
    
    print(f"\n[3] Sending test email to: {test_appointment['email']}")
    print("    Please wait...")
    
    try:
        success = await email_service.send_appointment_confirmation(
            test_appointment['email'],
            test_appointment
        )
        
        if success:
            print("\n✓✓✓ EMAIL SENT SUCCESSFULLY! ✓✓✓")
            print(f"\nCheck your inbox: {test_appointment['email']}")
            print("(Also check SPAM/Junk folder)")
        else:
            print("\n✗✗✗ EMAIL FAILED TO SEND ✗✗✗")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)

if __name__ == "__main__":
    asyncio.run(test_email())