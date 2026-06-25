from fastapi import APIRouter, HTTPException, Path
from app.models import AppointmentResponse
from app.db_client import get_appointment_by_id

router = APIRouter(prefix="/appointments", tags=["Appointment"])


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def read_appointment(
    appointment_id: int = Path(..., title="The ID of the appointment to fetch", gt=0),
):
    """
    GET /appointments/{appointment_id}
    Fetches an appointment by ID.

    Path Parameters:
    - appointment_id (int): Positive integer representing the appointment ID.

    Responses:
    - 200: Successful retrieval of the appointment.
    - 404: Appointment not found.
    """
    appointment = get_appointment_by_id(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return AppointmentResponse(**appointment)
