from fastapi import APIRouter, UploadFile, Form, HTTPException
import pandas as pd
import uuid
from memory import init_session, save_excel, save_credentials

router = APIRouter()

@router.post("/userdata")
async def user_data(
    file: UploadFile,
    sender_email: str = Form(...),
    sender_password: str = Form(...),
    email_column: str = Form(...)
):
    session_id = str(uuid.uuid4())
    init_session(session_id)

    if file.filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif file.filename.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file.file)
    else:
        raise HTTPException(status_code=400, detail="Only CSV or Excel supported")

    if email_column not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid email column")

    save_excel(
        session_id,
        schema=list(df.columns),
        rows=df.to_dict(orient="records")
    )
    save_credentials(session_id, sender_email, sender_password, email_column)
    

    return {
        "message": "Excel uploaded successfully",
        "session_id": session_id,
        "total_rows": len(df)
    }