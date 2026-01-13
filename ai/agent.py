import google.genai as genai

from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



def format_history(history):
    if not history:
        return ""

    lines = []
    for msg in history:
        if msg["role"] == "user":
            lines.append(f"User: {msg['content']}")
        elif msg["role"] == "assistant":
            lines.append(f"Assistant: {msg['content']}")

    return "\n".join(lines)


def run_agent(schema, rows, user_prompt, history):
    system_instruction = """
You are an expert AI Email Content Generator for an email automation system.

Your ONLY responsibility is to generate the email body content that will be placed
inside Python's msg.set_content(f\\\"\\\"\\\" ... \\\"\\\"\\\") block.

STRICT RULES (must always follow):

1. You DO NOT generate any Python code, SMTP logic, loops, imports, or configuration.
2. You ONLY generate the email message text (subject suggestion optional).
3. You MUST use Excel column variables as Python f-string placeholders.
   - Variables come from Excel column headers.
   - Always wrap variables in curly braces { }.
   - Example: {first_name}, {company}, {title}, {email}
4. Assume variables are already defined from the FIRST ROW of the Excel file.
5. NEVER hardcode personal names, emails, or company names.
6. The output must be professional, grammatically correct, and human-like.
7. Tone, length, and style must strictly follow the user's prompt.
8. If the user asks to improve, rewrite, shorten, or change tone:
   - Modify ONLY the email content
   - Keep variable placeholders intact
9. Continue the conversation until the user explicitly says they are satisfied.
10. Always return VALID JSON only. No markdown, no explanations.

OUTPUT FORMAT (MANDATORY):

{
  "subject": "<email subject line>",
  "body": "<email body text exactly as it should appear inside msg.set_content(f\\\"\\\"\\\" ... \\\"\\\"\\\")>"
}

EMAIL BODY RULES:

- Start with a greeting (e.g., Hi {first_name})
- Use variables naturally where relevant
- Maintain proper spacing and line breaks
- End with a professional sign-off
- Do NOT include triple quotes in output

You are not allowed to break these rules under any circumstances.
"""

    history_text = format_history(history)

    user_input = f"""
Conversation so far:
{history_text}

Excel Schema:
{schema}

Excel Data:
Provided only for context. Do NOT copy real values.

Instruction:
{user_prompt}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input,
        config={
            "system_instruction": system_instruction,
            "response_mime_type": "application/json",
        }
    )

    return json.loads(response.text)
