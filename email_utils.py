from email.message import EmailMessage
from pathlib import Path

def build_email_prompt(job_description):
    return f"""
You're a job seeker sending a cold email to an HR person. Based on the job description below, write a short, personalized, and professional email expressing interest.

Job Description:
{job_description}

Structure: Greeting → Why you're writing → Interest + Fit → Resume mention → Polite close.
"""

def extract_email_body(response_text):
    return response_text.strip()

def format_email(sender_email, recipient_email, body, resume_path=None):
    msg = EmailMessage()
    msg["Subject"] = "Application Inquiry Based on Job Description"
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(body)

    if resume_path:
        with open(resume_path, "rb") as f:
            file_data = f.read()
            file_name = Path(resume_path).name
            msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    return msg
