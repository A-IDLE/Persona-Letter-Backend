from fastapi import FastAPI, Depends, HTTPException,APIRouter
from starlette.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os

router = APIRouter()

# Configure the OAuth 2.0 Flow
CLIENT_SECRETS_FILE = "../googleOauthKey.json"  # Path to your client_secret.json file
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

flow = Flow.from_client_secrets_file(
    client_secrets_file=CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri='http://localhost:9000/callback'
)

@router.get("/sendmail")
def authenticate_user():
    authorization_url, state = flow.authorization_url()
    return RedirectResponse(authorization_url)

@router.get("/callback")
def callback(token: str):
    flow.fetch_token(authorization_response=token)
    credentials = flow.credentials
    try:
        service = build('gmail', 'v1', credentials=credentials)
        # Create message
        message = (service.users().messages().send(userId="me", body=message_body).execute())
        print('Message Id: %s' % message['id'])
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Define the message creation function
def create_message(sender, to, subject, message_text):
    from email.mime.text import MIMEText
    import base64
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode()}

# Create your email content
message_body = create_message("aidlepersonaletter@gmail.com", "isac7722@gmail.com", "Your Subject", "Email body text here")
