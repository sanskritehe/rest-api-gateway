from app.db_client import (
    create_appointment,
    get_all_appointments,
    update_appointment,
    get_appointment_by_id,
    delete_appointment_by_id
)


def book_appointment(data):
    # Add business rules or validation if needed
    return create_appointment(data)


def list_appointments(skip: int, limit: int):
    params = {"_start": skip, "_limit": limit}
    return get_all_appointments(params=params)


def update_booking(appointment_id: int, data):
    return update_appointment(appointment_id, data)


def get_appointment_by_id(appointment_id: int):
    return get_appointment_by_id(appointment_id)


def delete_appointment_by_id(appointment_id: int):
    return delete_appointment_by_id(appointment_id)

