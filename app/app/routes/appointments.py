from fastapi import APIRouter, HTTPException
from app.models import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.services.booking_service import (
    book_appointment,
    list_appointments,
    update_booking,
    cancel_booking,
    get_appointment_by_id
)

router = APIRouter(prefix="/appointments", tags=["Appointment"])


# Create a new appointment
@router.post("/")
def create_appointment(req: AppointmentCreate):
    return book_appointment(req.dict())


# Get all appointments
@router.get("/")
def get_appointments():
    return list_appointments()


# Get an appointment by ID
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment_by_id_route(appointment_id: int):
    appointment = get_appointment_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


# Update an appointment by ID
@router.put("/{appointment_id}")
def update_appointment_by_id(appointment_id: int, req: AppointmentUpdate):
    return update_booking(appointment_id, req.dict())


# Cancel an appointment by ID
@router.delete("/{appointment_id}")
def cancel_appointment_by_id(appointment_id: int):
    return cancel_booking(appointment_id)
