from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from langgraph_email_agent import run_email_agent
import shutil

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/send_email/")
async def send_email(
    job_description: str = Form(...),
    hr_email: str = Form(...),
    sender_email: str = Form(...),
    sender_app_password: str = Form(...),
    resume_file: UploadFile = None
):
    resume_path = None
    if resume_file:
        resume_path = f"temp_{resume_file.filename}"
        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(resume_file.file, buffer)

    response = run_email_agent(
        job_description=job_description,
        hr_email=hr_email,
        sender_email=sender_email,
        sender_app_password=sender_app_password,
        resume_path=resume_path
    )
    return {"status": "Email queued", "details": response}
