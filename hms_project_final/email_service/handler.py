
import json
import smtplib
from email.mime.text import MIMEText


def send_email(event, context):
    body = json.loads(event.get('body', '{}'))
    email_type = body.get('type')
    recipient = body.get('email') or body.get('patient_email')

    # SMTP Config (Update with your Gmail/SMTP details)
    msg = MIMEText(f"HMS Notification: {email_type} for appointment at {body.get('start_time')}")
    msg['Subject'] = "Hospital Management System Update"
    msg['From'] = "rajnipal972@gmail.com"
    msg['To'] = recipient

    # In a real setup, use actual SMTP server credentials here
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Email logic triggered successfully"})
    }