import json

def send_notification(event, context):
    try:
        data = json.loads(event.get('body', '{}'))
        email_type = data.get('type')  # 'WELCOME' or 'BOOKING'
        recipient = data.get('email')
        
        # In a real scenario, use AWS SES or SendGrid here
        message = f"Email logic triggered for {recipient} of type {email_type}"
        
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "success", "message": message})
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
