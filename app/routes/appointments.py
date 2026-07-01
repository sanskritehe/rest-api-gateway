from fastapi import APIRouter, HTTPException, Path
from app.models import AppointmentResponse
from app.graphql_client import run_query
from app.services.booking_service import delete_appointment_by_id

router = APIRouter(prefix="/appointments", tags=["Appointment"])


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def read_appointment(
    appointment_id: int = Path(..., title="The ID of the appointment", gt=0),
):
    """
    GET /appointments/{appointment_id}
    Retrieves an appointment by ID.

    Path Parameters:
    - appointment_id (int): Positive integer representing the appointment ID.

    Responses:
    - 200: Successful retrieval of the appointment.
    - 404: Appointment not found.
    """
    existing_appointment = run_query(
        """
    query ($id: Int!) {
        appointment(id: $id) {
            id
            patientName
            doctorName
            date
            status
        }
    }
    """,
        {"id": appointment_id},
    )

    if existing_appointment.get("data", {}).get("appointment") is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return AppointmentResponse(**existing_appointment["data"]["appointment"])


@router.delete("/{appointment_id}", response_model=dict)
def delete_appointment(
    appointment_id: int = Path(..., title="The ID of the appointment", gt=0),
):
    """
    DELETE /appointments/{appointment_id}
    Deletes an appointment by ID.

    Path Parameters:
    - appointment_id (int): Positive integer representing the appointment ID.

    Responses:
    - 200: Successful deletion of the appointment.
    - 404: Appointment not found.
    """
    deleted_appointment = delete_appointment_by_id(appointment_id)

    if deleted_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return {
        "message": "Appointment deleted successfully",
        "appointment_id": appointment_id,
    }
