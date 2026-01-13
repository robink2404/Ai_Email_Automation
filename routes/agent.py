from fastapi import APIRouter, Form, HTTPException
import json
from ai.agent import run_agent
from memory import get_history, add_message, get_excel

router = APIRouter()

@router.post("/draft")
async def draft_email(
    prompt: str = Form(...),
    session_id: str = Form(...)
):
    excel = get_excel(session_id)
    if not excel:
        raise HTTPException(status_code=404, detail="Excel not found for session")

    history = get_history(session_id)

    result = run_agent(
        schema=excel["schema"],
        rows=excel["rows"],
        user_prompt=prompt,
        history=history
    )

    add_message(session_id, "user", prompt)
    add_message(session_id, "assistant", json.dumps(result))

    return {
        "session_id": session_id,
        "response": result
    }