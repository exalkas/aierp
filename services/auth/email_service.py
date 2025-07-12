"""
Email Service for Authentication
Handles sending password reset and email verification emails
"""

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import Optional

from config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for authentication-related emails"""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_tls = settings.SMTP_TLS
        self.from_email = settings.FROM_EMAIL or "noreply@erp-system.gr"
    
    async def send_email(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str, 
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send email using SMTP
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.from_email
            message["To"] = to_email
            
            # Add text content if provided
            if text_content:
                text_part = MIMEText(text_content, "plain", "utf-8")
                message.attach(text_part)
            
            # Add HTML content
            html_part = MIMEText(html_content, "html", "utf-8")
            message.attach(html_part)
            
            # Send email
            if self.smtp_host and self.smtp_username and self.smtp_password:
                await aiosmtplib.send(
                    message,
                    hostname=self.smtp_host,
                    port=self.smtp_port,
                    start_tls=self.smtp_tls,
                    username=self.smtp_username,
                    password=self.smtp_password,
                )
                logger.info(f"Email sent successfully to: {to_email}")
                return True
            else:
                # Development mode - just log the email
                logger.info(f"[DEV MODE] Email would be sent to: {to_email}")
                logger.info(f"[DEV MODE] Subject: {subject}")
                logger.info(f"[DEV MODE] HTML Content: {html_content}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False


# Global email service instance
email_service = EmailService()


async def send_password_reset_email(email: str, full_name: str, reset_token: str) -> bool:
    """
    Send password reset email with reset link
    """
    try:
        # Create reset URL (in production, this would be your frontend URL)
        reset_url = f"http://localhost:3000/auth/reset-password?token={reset_token}"
        
        subject = "Επαναφορά Κωδικού Πρόσβασης - Greek ERP/CRM"
        
        # HTML email template
        html_content = f"""
        <!DOCTYPE html>
        <html lang="el">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Επαναφορά Κωδικού Πρόσβασης</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #0066CC 0%, #004499 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">Greek ERP/CRM</h1>
                <p style="color: #FFF700; margin: 10px 0 0 0; font-size: 16px;">Σύστημα Διαχείρισης Επιχειρήσεων</p>
            </div>
            
            <div style="background: white; padding: 40px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 10px 10px;">
                <h2 style="color: #0066CC; margin-bottom: 20px;">Γεια σας {full_name},</h2>
                
                <p style="font-size: 16px; margin-bottom: 20px;">
                    Λάβαμε αίτημα για επαναφορά του κωδικού πρόσβασης του λογαριασμού σας στο Greek ERP/CRM σύστημα.
                </p>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 30px 0;">
                    <p style="margin: 0; font-size: 14px; color: #666;">
                        Κάντε κλικ στο παρακάτω κουμπί για να επαναφέρετε τον κωδικό σας:
                    </p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" 
                       style="background: linear-gradient(135deg, #0066CC 0%, #004499 100%); 
                              color: white; 
                              padding: 15px 30px; 
                              text-decoration: none; 
                              border-radius: 8px; 
                              font-weight: bold; 
                              font-size: 16px; 
                              display: inline-block;
                              box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);">
                        Επαναφορά Κωδικού Πρόσβασης
                    </a>
                </div>
                
                <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 30px 0;">
                    <p style="margin: 0; font-size: 14px; color: #856404;">
                        <strong>Σημαντικό:</strong> Αυτός ο σύνδεσμος θα λήξει σε 24 ώρες για λόγους ασφαλείας.
                    </p>
                </div>
                
                <p style="font-size: 14px; color: #666; margin-top: 30px;">
                    Εάν δεν ζητήσατε επαναφορά κωδικού, παρακαλούμε αγνοήστε αυτό το email. 
                    Ο κωδικός σας θα παραμείνει ασφαλής.
                </p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <div style="text-align: center; color: #666; font-size: 12px;">
                    <p>Greek ERP/CRM System - Maritime Industry Solutions</p>
                    <p>© 2024 - Powered by Advanced Business Solutions</p>
                    <p style="margin-top: 15px;">
                        Για υποστήριξη επικοινωνήστε μαζί μας: support@erp-system.gr
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Text version for email clients that don't support HTML
        text_content = f"""
        Greek ERP/CRM - Επαναφορά Κωδικού Πρόσβασης
        
        Γεια σας {full_name},
        
        Λάβαμε αίτημα για επαναφορά του κωδικού πρόσβασης του λογαριασμού σας.
        
        Για να επαναφέρετε τον κωδικό σας, επισκεφθείτε την παρακάτω διεύθυνση:
        {reset_url}
        
        Αυτός ο σύνδεσμος θα λήξει σε 24 ώρες για λόγους ασφαλείας.
        
        Εάν δεν ζητήσατε επαναφορά κωδικού, παρακαλούμε αγνοήστε αυτό το email.
        
        Greek ERP/CRM System
        support@erp-system.gr
        """
        
        return await email_service.send_email(email, subject, html_content, text_content)
        
    except Exception as e:
        logger.error(f"Failed to send password reset email to {email}: {e}")
        return False


async def send_verification_email(email: str, full_name: str, verification_token: str) -> bool:
    """
    Send email verification email
    """
    try:
        # Create verification URL (in production, this would be your frontend URL)
        verification_url = f"http://localhost:3000/auth/verify-email?token={verification_token}"
        
        subject = "Επιβεβαίωση Email - Greek ERP/CRM"
        
        # HTML email template
        html_content = f"""
        <!DOCTYPE html>
        <html lang="el">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Επιβεβαίωση Email</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #0066CC 0%, #004499 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">Greek ERP/CRM</h1>
                <p style="color: #FFF700; margin: 10px 0 0 0; font-size: 16px;">Καλώς ήρθατε!</p>
            </div>
            
            <div style="background: white; padding: 40px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 10px 10px;">
                <h2 style="color: #0066CC; margin-bottom: 20px;">Καλώς ήρθατε {full_name}!</h2>
                
                <p style="font-size: 16px; margin-bottom: 20px;">
                    Σας ευχαριστούμε που εγγραφήκατε στο Greek ERP/CRM σύστημα. 
                    Για να ολοκληρώσετε την εγγραφή σας, παρακαλούμε επιβεβαιώστε τη διεύθυνση email σας.
                </p>
                
                <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 30px 0; border-left: 4px solid #28a745;">
                    <p style="margin: 0; font-size: 14px; color: #155724;">
                        <strong>Τι θα κερδίσετε:</strong><br>
                        • Πλήρη πρόσβαση στο σύστημα διαχείρισης<br>
                        • Ελληνική συμμόρφωση AADE<br>
                        • Αυτόματη έκδοση παραστατικών<br>
                        • Διαχείριση πελατών και προμηθευτών
                    </p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" 
                       style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                              color: white; 
                              padding: 15px 30px; 
                              text-decoration: none; 
                              border-radius: 8px; 
                              font-weight: bold; 
                              font-size: 16px; 
                              display: inline-block;
                              box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);">
                        Επιβεβαίωση Email
                    </a>
                </div>
                
                <div style="background: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 8px; margin: 30px 0;">
                    <p style="margin: 0; font-size: 14px; color: #0c5460;">
                        <strong>Σημείωση:</strong> Αυτός ο σύνδεσμος θα λήξει σε 48 ώρες.
                    </p>
                </div>
                
                <p style="font-size: 14px; color: #666; margin-top: 30px;">
                    Εάν δεν εγγραφήκατε για αυτό το λογαριασμό, παρακαλούμε αγνοήστε αυτό το email.
                </p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <div style="text-align: center; color: #666; font-size: 12px;">
                    <p>Greek ERP/CRM System - Maritime Industry Solutions</p>
                    <p>© 2024 - Powered by Advanced Business Solutions</p>
                    <p style="margin-top: 15px;">
                        Για υποστήριξη επικοινωνήστε μαζί μας: support@erp-system.gr
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Text version
        text_content = f"""
        Greek ERP/CRM - Επιβεβαίωση Email
        
        Καλώς ήρθατε {full_name}!
        
        Σας ευχαριστούμε που εγγραφήκατε στο Greek ERP/CRM σύστημα.
        
        Για να ολοκληρώσετε την εγγραφή σας, επισκεφθείτε την παρακάτω διεύθυνση:
        {verification_url}
        
        Αυτός ο σύνδεσμος θα λήξει σε 48 ώρες.
        
        Εάν δεν εγγραφήκατε για αυτό το λογαριασμό, παρακαλούμε αγνοήστε αυτό το email.
        
        Greek ERP/CRM System
        support@erp-system.gr
        """
        
        return await email_service.send_email(email, subject, html_content, text_content)
        
    except Exception as e:
        logger.error(f"Failed to send verification email to {email}: {e}")
        return False 