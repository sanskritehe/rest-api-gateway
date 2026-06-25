from fastapi import APIRouter, HTTPException, Path
from app.models import AppointmentResponse
from app.graphql_client import run_query

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
    query = """
    query getAppointment($id: Int!) {
        appointment(id: $id) {
            id
            user
            time
            status
        }
    }
    """
    variables = {"id": appointment_id}
    result = run_query(query, variables)

    if result.get("errors", []):
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment = result.get("data", {}).get("appointment")

    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return AppointmentResponse(**appointment)
