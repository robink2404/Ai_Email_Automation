MAX_HISTORY = 10
SESSION_MEMORY = {}

def init_session(session_id):
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = {
            "history": [],
            "excel": None,
            "credentials": None
        }

def save_credentials(session_id, email, password, column):
    init_session(session_id)
    SESSION_MEMORY[session_id]["credentials"] = {
        "sender_email": email,
        "sender_password": password,
        "email_column": column
    }

def get_credentials(session_id):
    session = SESSION_MEMORY.get(session_id)
    if not session:
        return None
    return session.get("credentials")

def get_history(session_id):
    session = SESSION_MEMORY.get(session_id)
    if not session:
        return []
    return session["history"]

def add_message(session_id, role, content):
    init_session(session_id)
    history = SESSION_MEMORY[session_id]["history"]
    history.append({"role": role, "content": content})
    SESSION_MEMORY[session_id]["history"] = history[-MAX_HISTORY:]

def save_excel(session_id, schema, rows):
    init_session(session_id)
    SESSION_MEMORY[session_id]["excel"] = {
        "schema": schema,
        "rows": rows
    }

def get_excel(session_id):
    session = SESSION_MEMORY.get(session_id)
    if not session or not session["excel"]:
        return None
    return session["excel"]
