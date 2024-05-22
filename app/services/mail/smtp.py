import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


from fastapi import APIRouter

router = APIRouter()

# Get environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_EMAIL = os.getenv('SMTP_EMAIL')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')


def send_email(to_email: str):
    # SMTP server configuration
    smtp_server = SMTP_SERVER
    port = SMTP_PORT
    from_email = SMTP_EMAIL
    password = SMTP_PASSWORD

    # Sanitize password
    password = password.replace(u'\xa0', ' ').strip()

    # Create the email content
    subject = "This is subject"
    body = """
        <html>
            <body>
                <p>Your Letter has arrived!</p>
                <p>Visit our homepage: <a href="http://localhost:3000/">Persona Letter</a></p>
            </body>
        </html>
        """
    

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(body, 'html'))
    
    try:
        # Create server object with SSL option
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Secure the connection
        server.login(from_email, password)  # Log in to your email account
        text = msg.as_string()  # Convert the message to a string
        server.sendmail(from_email, to_email, text)  # Send the email
        server.quit()  # Quit the server
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


