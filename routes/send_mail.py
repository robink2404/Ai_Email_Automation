from fastapi import APIRouter, HTTPException
from memory import get_credentials, get_excel
import smtplib
import time
from email.message import EmailMessage

router = APIRouter()


@router.post("/send/{session_id}")
async def send_emails(session_id: str):
    creds = get_credentials(session_id)
    excel_data = get_excel(session_id)

    if not creds or not excel_data:
        raise HTTPException(
            status_code=404,
            detail="Session data not found"
        )

    sender_email = creds["sender_email"]
    sender_password = creds["sender_password"]
    email_col = creds["email_column"]

    rows = excel_data["rows"]
    schema = excel_data["schema"]

    # Connect SMTP
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Login failed: {e}")

    sent = 0
    failed = 0

    for row in rows:
        if not row.get(email_col):
            continue

        try:
            # Build variables dynamically
            variables = {
                col.lower().replace(" ", "_"): str(row[col]).strip()
                for col in schema
            }

            msg = EmailMessage()
            msg["From"] = sender_email
            msg["To"] = variables[email_col.lower().replace(" ", "_")]
            msg["Subject"] = "Frontend Developer | React, TypeScript"

            msg.set_content(f"""
Hi {variables.get("name", "")},

I hope you are doing well.

This email was sent using AI Mail Agent.

Best regards,
Robin Kumar
""")

            server.send_message(msg)
            sent += 1
            time.sleep(5)

        except Exception as e:
            print("Failed:", e)
            failed += 1

    server.quit()

    return {
        "status": "completed",
        "sent": sent,
        "failed": failed
    }
