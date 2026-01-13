from fastapi import APIRouter, HTTPException
from memory import get_credentials, get_excel
import re

router = APIRouter()


def to_var_name(col: str) -> str:
    """Convert Excel column header to safe python variable"""
    col = col.strip().lower()
    col = re.sub(r"[^a-z0-9_ ]", "", col)
    return col.replace(" ", "_")


@router.get("/generate_script/{session_id}")
async def generate_user_script(session_id: str):
    # 1. Retrieve session data
    creds = get_credentials(session_id)
    excel_data = get_excel(session_id)

    if not creds or not excel_data:
        raise HTTPException(
            status_code=404,
            detail="Session data not found. Please upload Excel and credentials first."
        )

    schema = excel_data["schema"]          # Excel headers
    rows = excel_data["rows"]
    email_col = creds.get("email_column")

    if not email_col:
        raise HTTPException(
            status_code=400,
            detail="Email column missing. Please select email column again."
        )

    # 2. Generate variable assignments from Excel columns
    variable_assignments = ""
    column_variables = []

    for col in schema:
        var_name = to_var_name(col)
        column_variables.append({
            "column": col,
            "variable": var_name
        })
        variable_assignments += (
            f"        {var_name} = str(row[\"{col}\"]).strip()\n"
        )

    # 3. Build script
    script_template = f"""s
"""

    return {
        "session_id": session_id,
        "columns": schema,
        "variables": column_variables,
        "email_column": email_col,
        "script_preview": script_template
    }
