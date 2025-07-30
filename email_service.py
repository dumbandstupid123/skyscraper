import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
import sendgrid
from sendgrid.helpers.mail import Mail
from twilio.rest import Client as TwilioClient

logger = logging.getLogger(__name__)

class EmailService:
    """Handles email sending for client communication."""
    
    def __init__(self):
        self.sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
        self.from_email = os.environ.get('FROM_EMAIL', 'nextstep@yourdomain.com')
        self.from_name = os.environ.get('FROM_NAME', 'NextStep Support Team')
        
        # Twilio SMS configuration
        self.twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
        self.twilio_client = None
        
        if self.twilio_account_sid and self.twilio_auth_token:
            try:
                self.twilio_client = TwilioClient(self.twilio_account_sid, self.twilio_auth_token)
            except Exception as e:
                logger.warning(f"Failed to initialize Twilio client: {e}")
        
    async def send_needs_assessment_form(self, client_data: Dict[str, Any], form_url: str) -> bool:
        """Send needs assessment form to a client."""
        try:
            client_email = client_data.get('email', '')
            client_name = f"{client_data.get('firstName', '')} {client_data.get('lastName', '')}"
            
            if not client_email:
                logger.error("Client email not found")
                return False
            
            # Create email content
            subject = "NextStep - Your Personalized Needs Assessment"
            
            html_content = self._create_needs_assessment_email_html(client_name, form_url)
            text_content = self._create_needs_assessment_email_text(client_name, form_url)
            
            # Send email using SendGrid if available, otherwise use SMTP
            if self.sendgrid_api_key:
                return await self._send_via_sendgrid(client_email, subject, html_content, text_content)
            else:
                return await self._send_via_smtp(client_email, subject, html_content, text_content)
                
        except Exception as e:
            logger.error(f"Failed to send needs assessment form: {e}")
            return False
    
    async def _send_via_sendgrid(self, to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using SendGrid."""
        try:
            sg = sendgrid.SendGridAPIClient(api_key=self.sendgrid_api_key)
            
            message = Mail(
                from_email=(self.from_email, self.from_name),
                to_emails=to_email,
                subject=subject,
                html_content=html_content,
                plain_text_content=text_content
            )
            
            response = sg.send(message)
            logger.info(f"Email sent via SendGrid. Status: {response.status_code}")
            return response.status_code == 202
            
        except Exception as e:
            logger.error(f"SendGrid email failed: {e}")
            return False
    
    async def _send_via_smtp(self, to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using SMTP (fallback method)."""
        try:
            smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.environ.get('SMTP_PORT', '587'))
            smtp_username = os.environ.get('SMTP_USERNAME')
            smtp_password = os.environ.get('SMTP_PASSWORD')
            
            if not smtp_username or not smtp_password:
                logger.warning("SMTP credentials not configured")
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{smtp_username}>"
            msg['To'] = to_email
            
            # Attach parts
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent via SMTP to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"SMTP email failed: {e}")
            return False
    
    def _create_needs_assessment_email_html(self, client_name: str, form_url: str) -> str:
        """Create HTML email content for needs assessment."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>NextStep - Needs Assessment</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .button {{ 
                    display: inline-block; 
                    background-color: #16a34a; 
                    color: white; 
                    padding: 12px 24px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    margin: 20px 0;
                }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>NextStep Support Services</h1>
                </div>
                <div class="content">
                    <h2>Hello {client_name},</h2>
                    <p>We hope this message finds you well. As part of our commitment to providing you with the best possible support, we'd like to better understand your current needs and how we can assist you.</p>
                    
                    <p>Please take a few minutes to complete our quick needs assessment. This will help us:</p>
                    <ul>
                        <li>Understand your current housing, food, and transportation needs</li>
                        <li>Prioritize the most urgent assistance you need</li>
                        <li>Connect you with the right resources and programs</li>
                        <li>Provide more personalized support</li>
                    </ul>
                    
                    <p>The form is quick and easy - just 11 questions that focus on your most essential needs.</p>
                    
                    <div style="text-align: center;">
                        <a href="{form_url}" class="button">Complete Your Needs Assessment</a>
                    </div>
                    
                    <p>If you have any questions or need assistance completing the form, please don't hesitate to contact us.</p>
                    
                    <p>Thank you for allowing us to support you on your journey.</p>
                    
                    <p>Best regards,<br>
                    The NextStep Support Team</p>
                </div>
                <div class="footer">
                    <p>This email was sent by NextStep Support Services. If you no longer wish to receive these emails, please contact us.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_needs_assessment_email_text(self, client_name: str, form_url: str) -> str:
        """Create plain text email content for needs assessment."""
        return f"""
Hello {client_name},

We hope this message finds you well. As part of our commitment to providing you with the best possible support, we'd like to better understand your current needs and how we can assist you.

Please take a few minutes to complete our quick needs assessment. This will help us:

- Understand your current housing, food, and transportation needs
- Prioritize the most urgent assistance you need  
- Connect you with the right resources and programs
- Provide more personalized support

The form is quick and easy - just 11 questions that focus on your most essential needs.

Complete your needs assessment here: {form_url}

If you have any questions or need assistance completing the form, please don't hesitate to contact us.

Thank you for allowing us to support you on your journey.

Best regards,
The NextStep Support Team

---
This email was sent by NextStep Support Services. If you no longer wish to receive these emails, please contact us.
        """
    
    async def send_email(self, to_email: str, subject: str, message: str, from_name: str = None) -> bool:
        """Send a generic email message."""
        try:
            # Use provided from_name or default
            sender_name = from_name or self.from_name
            
            # Create simple HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>NextStep Support Services</h1>
                    </div>
                    <div class="content">
                        {message.replace(chr(10), '<br>')}
                    </div>
                    <div class="footer">
                        <p>This email was sent by {sender_name} via NextStep Support Services.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_content = f"{message}\n\n---\nThis email was sent by {sender_name} via NextStep Support Services."
            
            # Send email using configured method
            if self.sendgrid_api_key:
                return await self._send_via_sendgrid(to_email, subject, html_content, text_content)
            else:
                return await self._send_via_smtp(to_email, subject, html_content, text_content)
                
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    async def send_sms(self, to_phone: str, message: str, from_name: str = None) -> bool:
        """Send an SMS message using Twilio."""
        try:
            if not self.twilio_client:
                logger.error("Twilio client not configured. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER")
                return False
            
            if not self.twilio_phone_number:
                logger.error("Twilio phone number not configured")
                return False
            
            # Clean phone number (remove any formatting)
            clean_phone = ''.join(filter(str.isdigit, to_phone))
            
            # Add +1 if it's a US number without country code
            if len(clean_phone) == 10:
                clean_phone = f"+1{clean_phone}"
            elif len(clean_phone) == 11 and clean_phone.startswith('1'):
                clean_phone = f"+{clean_phone}"
            elif not clean_phone.startswith('+'):
                clean_phone = f"+{clean_phone}"
            
            # Prepare message with sender info
            sender_name = from_name or self.from_name
            full_message = f"{message}\n\n- {sender_name} via NextStep"
            
            # Send SMS
            message_obj = self.twilio_client.messages.create(
                body=full_message,
                from_=self.twilio_phone_number,
                to=clean_phone
            )
            
            logger.info(f"SMS sent successfully. SID: {message_obj.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS: {e}")
            return False

    async def make_voice_call(self, to_phone: str, message: str, client_name: str = None, from_name: str = None) -> bool:
        """Make a voice call using Twilio Voice API with AI agent reading the message."""
        try:
            if not self.twilio_client:
                logger.error("Twilio client not configured. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER")
                return False
            
            if not self.twilio_phone_number:
                logger.error("Twilio phone number not configured")
                return False
            
            # Clean phone number (remove any formatting)
            clean_phone = ''.join(filter(str.isdigit, to_phone))
            
            # Add +1 if it's a US number without country code
            if len(clean_phone) == 10:
                clean_phone = f"+1{clean_phone}"
            elif len(clean_phone) == 11 and clean_phone.startswith('1'):
                clean_phone = f"+{clean_phone}"
            elif not clean_phone.startswith('+'):
                clean_phone = f"+{clean_phone}"
            
            # Prepare the voice message
            sender_name = from_name or self.from_name
            client_info = f"regarding {client_name}" if client_name else ""
            
            # Create TwiML for the voice call with simple, working syntax
            voice_script = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna-Neural" language="en-US">
        Hey {client_name}! I'm calling from NextStep.
        <break time="1s"/>
        {message}
        <break time="1s"/>
        If you have any questions or need anything at all, please don't hesitate to call me back. Have a wonderful day!
    </Say>
</Response>"""
            
            # Make the voice call
            logger.info(f"Initiating call to {clean_phone} with TwiML: {voice_script[:200]}...")
            call = self.twilio_client.calls.create(
                twiml=voice_script,
                to=clean_phone,
                from_=self.twilio_phone_number
            )
            
            logger.info(f"Voice call initiated successfully. Call SID: {call.sid}, Status: {call.status}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to make voice call: {e}")
            return False
    
    async def send_notification_to_staff(self, client_name: str, form_response: Dict[str, Any]) -> bool:
        """Send notification to staff when a client submits a needs assessment."""
        try:
            staff_email = os.environ.get('STAFF_NOTIFICATION_EMAIL', self.from_email)
            subject = f"New Needs Assessment Submitted - {client_name}"
            
            # Create summary of client needs
            needs_summary = []
            assessment = form_response.get('needs_assessment', {})
            
            for category, details in assessment.items():
                if isinstance(details, dict) and details.get('needed'):
                    needs_summary.append(category.title())
            
            html_content = f"""
            <h2>New Needs Assessment Submitted</h2>
            <p><strong>Client:</strong> {client_name}</p>
            <p><strong>Email:</strong> {form_response.get('client_email', 'N/A')}</p>
            <p><strong>Submitted:</strong> {form_response.get('timestamp', 'N/A')}</p>
            
            <h3>Requested Services:</h3>
            <ul>
                {''.join([f'<li>{need}</li>' for need in needs_summary])}
            </ul>
            
            <h3>Additional Notes:</h3>
            <p>{form_response.get('additional_notes', 'None provided')}</p>
            
            <p>Please log into the NextStep dashboard to review the full assessment and update the client's profile.</p>
            """
            
            text_content = f"""
New Needs Assessment Submitted

Client: {client_name}
Email: {form_response.get('client_email', 'N/A')}
Submitted: {form_response.get('timestamp', 'N/A')}

Requested Services:
{chr(10).join([f'- {need}' for need in needs_summary])}

Additional Notes:
{form_response.get('additional_notes', 'None provided')}

Please log into the NextStep dashboard to review the full assessment and update the client's profile.
            """
            
            if self.sendgrid_api_key:
                return await self._send_via_sendgrid(staff_email, subject, html_content, text_content)
            else:
                return await self._send_via_smtp(staff_email, subject, html_content, text_content)
                
        except Exception as e:
            logger.error(f"Failed to send staff notification: {e}")
            return False 