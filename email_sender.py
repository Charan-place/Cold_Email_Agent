from celery import Celery
import smtplib
from email.message import EmailMessage
from email_utils import format_email

app = Celery("email_sender", broker="redis://localhost:6379/0")

@app.task
def send_email_task(sender_email, sender_password, recipient_email, email_body, resume_path=None):
    msg = format_email(sender_email, recipient_email, email_body, resume_path)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return "Email sent successfully."
    except Exception as e:
        return f"Failed to send email: {str(e)}"
