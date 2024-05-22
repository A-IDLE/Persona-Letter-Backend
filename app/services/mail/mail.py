from fastapi import APIRouter
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64



router = APIRouter()

@router.get("/sendmail")
def send_mail():
    service = gmail_authenticate()
    email_body = create_message("aidlepersonaletter@gmail.com", "isac7722@example.com", "Hello from Gmail API", "Hello, this is a test email.")
    send_message(service, "me", email_body)
    


def gmail_authenticate():
    # Load the credentials and create an authorized Gmail API service
    flow = InstalledAppFlow.from_client_secrets_file('../googleOauthKey.json', scopes=['https://www.googleapis.com/auth/gmail.send'])
    credentials = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=credentials)
    return service

def create_message(sender, to, subject, message_text):
    # Create a message to send
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode()}

def send_message(service, user_id, message):
    # Send the message via Gmail API
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')

# Example usage
# service = gmail_authenticate()
# email_body = create_message("aidlepersonaletter@gmail.com", "isac7722@example.com", "Hello from Gmail API", "Hello, this is a test email.")
# send_message(service, "me", email_body)