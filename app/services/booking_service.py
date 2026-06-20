from typing import List, Optional
from app.db_client import (
    get_all_appointments,
    get_appointment_by_id as db_get_appointment_by_id,
    delete_appointment,
)


def list_appointments() -> List[dict]:
    return get_all_appointments()


def get_appointment_by_id(appointment_id: int) -> Optional[dict]:
    return db_get_appointment_by_id(appointment_id)


def delete_appointment_service(appointment_id: int) -> bool:
    """
    Deletes an appointment by its ID. First checks if the appointment exists, and
    then calls the database client to perform a hard delete operation.

    Args:
        appointment_id (int): The ID of the appointment to delete.

    Returns:
        bool: True if the appointment was successfully deleted, False if not found.
    """
    existing_appointment = get_appointment_by_id(appointment_id)
    if not existing_appointment:
        return False
    return delete_appointment(appointment_id)
