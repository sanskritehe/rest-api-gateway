from typing import List
from app.db_client import get_all_appointments, get_appointment_by_id, delete_appointment


def list_appointments() -> List[dict]:
    return get_all_appointments()


def delete_appointment_service(appointment_id: int) -> bool:
    existing_appointment = get_appointment_by_id(appointment_id)
    if not existing_appointment:
        return False
    return delete_appointment(appointment_id)
