from app.db_client import fetch_appointment

def get_appointment(id: int):
    return fetch_appointment(id)
