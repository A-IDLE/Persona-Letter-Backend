import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import os
from dotenv import load_dotenv
from requests import Session

from models.models import Letter
from services.image.generate import image_questions

load_dotenv()

# AWS SQS 클라이언트 설정
sqs = boto3.client(
    'sqs',
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("CREDENTIALS_ACCESS_KEY"),
	aws_secret_access_key=os.getenv("CREDENTIALS_SECRET_KEY"),
)

# SQS 대기열 URL 설정
QUEUE_URL = os.getenv("AWS_QUEUE_URL")

def sqs_message(letter_content, letter_id) -> None:
    try:
        keywords = image_questions(letter_content)
        print(f"sqs_message keywords : {keywords}")
        print(f"\nsqs_message letter_id : {letter_id}")
        message = {
            'keywords': keywords,
            'letter_id': letter_id
        }
        message = json.dumps(message) # JSON 형식으로 변환
        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=message
        )
        print(f"\nMessage sent with ID: {response['MessageId']}")
    except (BotoCoreError, ClientError) as error:
        print(f"Failed to send message: {error}")
