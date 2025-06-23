import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import certifi

load_dotenv()
os.environ['SSL_CERT_FILE'] = certifi.where()

# Use SendGrid API to send daily digest email
def send_email(subject, content):
    message = Mail(
        from_email=os.getenv("FROM_EMAIL"),
        to_emails=os.getenv("TO_EMAIL"),
        subject=subject,
        plain_text_content=content
    )
    try:
        sendgrid = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sendgrid.send(message)
        print(f"Email sent! Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Testing
if __name__ == "__main__":
    send_email("Daily Digest", "Hello, here's your digest content.")
