from langgraph.graph import StateGraph, END
from email_sender import send_email_task
from email_utils import build_email_prompt, extract_email_body
from db import log_email
import os
import google.generativeai as genai
from typing import TypedDict, Optional

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
print("✅ GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))  # Debug print
# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Define the input/output schema
class EmailState(TypedDict):
    job_description: str
    hr_email: str
    sender_email: str
    sender_app_password: str
    email_body: Optional[str]
    resume_path: Optional[str]

# ✅ Generate email from Gemini
def generate_email_node(state: EmailState) -> EmailState:
    prompt = build_email_prompt(state["job_description"])
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    email_body = extract_email_body(response.text)
    state["email_body"] = email_body
    return state

# ✅ Queue the email to be sent via Celery
def send_email_node(state: EmailState) -> EmailState:
    send_email_task.delay(
        sender_email=state["sender_email"],
        sender_password=state["sender_app_password"],
        recipient_email=state["hr_email"],
        email_body=state["email_body"],
        resume_path=state.get("resume_path")
    )
    log_email(state["sender_email"], state["hr_email"], state["job_description"], state["email_body"])
    return state

# ✅ Main runner
def run_email_agent(job_description, hr_email, sender_email, sender_app_password, resume_path=None):
    g = StateGraph(EmailState)  # ✅ Fixed this line!
    g.add_node("generate_email", generate_email_node)
    g.add_node("send_email", send_email_node)
    g.set_entry_point("generate_email")
    g.add_edge("generate_email", "send_email")
    g.add_edge("send_email", END)
    app = g.compile()
    result = app.invoke({
        "job_description": job_description,
        "hr_email": hr_email,
        "sender_email": sender_email,
        "sender_app_password": sender_app_password,
        "resume_path": resume_path
    })
    return result
