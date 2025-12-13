import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket

class EmailNotifier:
    def __init__(self, smtp_host, smtp_port, sender_email, password, recipient_email):
        self.smtp_host = smtp_host
        self.smtp_port = int(smtp_port) if smtp_port else 587
        self.sender_email = sender_email
        self.password = password
        self.recipient_email = recipient_email

    def send_email(self, subject, body, image_data=None):
        if not self.smtp_host or not self.sender_email or not self.recipient_email:
            print("❌ EmailNotifier: Missing configuration")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))
            
            # TODO: Attach image if needed (skipping for now to stick to basic text alert first)
            # if image_data: ...

            # Connect to SMTP Server
            # Try/Except specifically for timeout/connection issues
            try:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10)
                server.starttls()  # Secure the connection
                server.login(self.sender_email, self.password)
                server.send_message(msg)
                server.quit()
                print(f"✅ Email sent to {self.recipient_email}")
                return True
            except smtplib.SMTPAuthenticationError:
                print("❌ Email Error: Authentication failed. Check password/app password.")
                return False
            except socket.gaierror:
                print("❌ Email Error: Invalid SMTP Host.")
                return False
            except Exception as e:
                print(f"❌ Email Sending Error: {e}")
                return False

        except Exception as e:
            print(f"❌ EmailNotifier Error: {e}")
            return False
