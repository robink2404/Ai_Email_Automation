from fastapi import APIRouter, Form, HTTPException, BackgroundTasks
from memory import get_credentials, get_excel
from email.message import EmailMessage
import smtplib
import pandas as pd
import time
import re

router = APIRouter()


def to_var_name(col: str) -> str:
    col = col.strip().lower()
    col = re.sub(r"[^a-z0-9_ ]", "", col)
    return col.replace(" ", "_")


def send_emails(creds, excel_data, subject, body):
    schema = excel_data["schema"]
    rows = excel_data["rows"]
    email_col = creds["email_column"]

    df = pd.DataFrame(rows)
    df = df[df[email_col].notna()]

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(creds["sender_email"], creds["sender_password"])
    print("✅ Logged in")

    for _, row in df.iterrows():
        variables = {
            to_var_name(col): str(row[col]).strip()
            for col in schema
        }

        msg = EmailMessage()
        msg["From"] = creds["sender_email"]
        msg["To"] = variables[to_var_name(email_col)]
        msg["Subject"] = subject.format(**variables)
        msg.set_content(body.format(**variables))

        try:
            server.send_message(msg)
            print(f"✅ Sent to {variables[to_var_name(email_col)]}")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Failed for {variables[to_var_name(email_col)]}: {e}")

    server.quit()
    print("🎉 Email automation completed")


@router.post("/finalize-script")
async def finalize_script(
    background_tasks: BackgroundTasks,
    session_id: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...)
):
    creds = get_credentials(session_id)
    excel_data = get_excel(session_id)

    if not creds or not excel_data:
        raise HTTPException(status_code=404, detail="Session data not found")

    background_tasks.add_task(
        send_emails,
        creds,
        excel_data,
        subject,
        body
    )

    return {
        "session_id": session_id,
        "status": "started",
        "message": "Emails are being sent in the background"
    }
