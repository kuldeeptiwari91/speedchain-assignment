import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    """Email service for sending appointment confirmations"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.email = os.getenv("SMTP_EMAIL")
        self.password = os.getenv("SMTP_PASSWORD")
        
        # ✅ Log initialization
        print(f"[Email Init] SMTP Server: {self.smtp_server}:{self.smtp_port}")
        print(f"[Email Init] From Email: {self.email if self.email else '❌ NOT SET'}")
        print(f"[Email Init] Password: {'✓ SET' if self.password else '❌ NOT SET'}")
    
    async def send_appointment_confirmation(self, to_email: str, appointment_details: dict) -> bool:
        """Send appointment confirmation email"""
        try:
            # ✅ Better credential check with clear logging
            if not self.email or not self.password:
                print("\n" + "="*60)
                print("[Email] ❌ EMAIL CREDENTIALS NOT CONFIGURED!")
                print("[Email] Please add to backend/.env:")
                print("[Email]   SMTP_EMAIL=your_email@gmail.com")
                print("[Email]   SMTP_PASSWORD=your_app_password")
                print("="*60 + "\n")
                return False
            
            # ✅ Log email attempt
            print(f"\n{'📧'*30}")
            print(f"[Email] Sending appointment confirmation...")
            print(f"[Email] To: {to_email}")
            print(f"[Email] From: {self.email}")
            print(f"[Email] Details: {appointment_details}")
            print(f"{'📧'*30}\n")
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Appointment Confirmation - SmileCare Dental"
            msg['From'] = self.email
            msg['To'] = to_email
            
            # Create HTML content
            html = f"""
            <html>
              <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                  <h2 style="color: #667eea; margin-top: 0;">✓ Appointment Confirmed!</h2>
                  
                  <p>Dear <strong>{appointment_details.get('name', 'Patient')}</strong>,</p>
                  
                  <p>Your appointment at <strong>SmileCare Dental</strong> has been successfully confirmed.</p>
                  
                  <div style="background-color: #f8f9fa; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #333;">Appointment Details:</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                      <tr>
                        <td style="padding: 8px 0;"><strong>Service:</strong></td>
                        <td style="padding: 8px 0;">{appointment_details.get('service', 'N/A')}</td>
                      </tr>
                      <tr>
                        <td style="padding: 8px 0;"><strong>Date:</strong></td>
                        <td style="padding: 8px 0;">{appointment_details.get('date', 'N/A')}</td>
                      </tr>
                      <tr>
                        <td style="padding: 8px 0;"><strong>Time:</strong></td>
                        <td style="padding: 8px 0;">{appointment_details.get('time', 'N/A')}</td>
                      </tr>
                      <tr>
                        <td style="padding: 8px 0;"><strong>Dentist:</strong></td>
                        <td style="padding: 8px 0;">{appointment_details.get('dentist', 'To be assigned')}</td>
                      </tr>
                    </table>
                  </div>
                  
                  <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>📍 Location:</strong> 123 Healthcare Ave, Downtown</p>
                    <p style="margin: 10px 0 0 0;"><strong>📞 Phone:</strong> (555) 123-4567</p>
                  </div>
                  
                  <p style="color: #7f8c8d; font-size: 14px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                    <strong>Important:</strong> If you need to reschedule or cancel, please call us at least 24 hours in advance.
                  </p>
                  
                  <p style="margin-top: 20px;">
                    Best regards,<br>
                    <strong>SmileCare Dental Team</strong>
                  </p>
                </div>
              </body>
            </html>
            """
            
            part = MIMEText(html, 'html')
            msg.attach(part)
            
            # ✅ Send with detailed logging and timeout
            print(f"[Email] Connecting to {self.smtp_server}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                print(f"[Email] Starting TLS encryption...")
                server.starttls()
                
                print(f"[Email] Authenticating as {self.email}...")
                server.login(self.email, self.password)
                
                print(f"[Email] Sending message...")
                server.send_message(msg)
            
            # ✅ Clear success message
            print(f"\n{'✅'*30}")
            print(f"[Email] ✅✅✅ EMAIL SENT SUCCESSFULLY! ✅✅✅")
            print(f"[Email] Recipient: {to_email}")
            print(f"[Email] Check inbox (and spam folder)")
            print(f"{'✅'*30}\n")
            return True
            
        # ✅ Specific error handling
        except smtplib.SMTPAuthenticationError as e:
            print(f"\n{'❌'*30}")
            print(f"[Email] ❌ AUTHENTICATION FAILED!")
            print(f"[Email] Error: {e}")
            print(f"[Email] Check:")
            print(f"[Email]   1. SMTP_EMAIL is correct")
            print(f"[Email]   2. SMTP_PASSWORD is App Password (not regular password)")
            print(f"[Email]   3. Get App Password: https://myaccount.google.com/apppasswords")
            print(f"{'❌'*30}\n")
            return False
            
        except smtplib.SMTPException as e:
            print(f"\n{'❌'*30}")
            print(f"[Email] ❌ SMTP ERROR: {e}")
            print(f"{'❌'*30}\n")
            return False
            
        except Exception as e:
            print(f"\n{'❌'*30}")
            print(f"[Email] ❌ UNEXPECTED ERROR!")
            print(f"[Email] Error type: {type(e).__name__}")
            print(f"[Email] Error message: {str(e)}")
            print(f"[Email] Full traceback:")
            import traceback
            traceback.print_exc()
            print(f"{'❌'*30}\n")
            return False