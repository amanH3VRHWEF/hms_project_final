import json
import smtplib
import os
from email.mime.text import MIMEText

def send_email(event, context):
    try:
        # Parse the body from the Django request
        body = json.loads(event.get('body', '{}'))
        recipient_email = body.get('email')
        notification_type = body.get('type')

        if not recipient_email or notification_type != "BOOKING_CONFIRMATION":
            return {"statusCode": 400, "body": json.dumps({"message": "Invalid payload"})}

        # SMTP Configuration (Use Environment Variables for Security)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.environ.get('EMAIL_USER')
        sender_password = os.environ.get('EMAIL_PASSWORD') # Use App Password

        # Create the Email Content
        msg = MIMEText(f"Hello, your appointment booking is confirmed for {body.get('slot_details')}.")
        msg['Subject'] = "Appointment Confirmation"
        msg['From'] = sender_email
        msg['To'] = recipient_email

        # Send via SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent successfully!"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
