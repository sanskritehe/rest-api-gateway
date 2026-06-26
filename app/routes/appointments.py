from fastapi import APIRouter, HTTPException, Path
from app.models import AppointmentResponse, AppointmentUpdate
from app.db_client import update_appointment_data
from app.graphql_client import run_query

router = APIRouter(prefix="/appointments", tags=["Appointment"])


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    update_data: AppointmentUpdate,
    appointment_id: int = Path(..., title="The ID of the appointment to update", gt=0),
):
    """
    PATCH /appointments/{appointment_id}
    Updates an appointment by ID.

    Path Parameters:
    - appointment_id (int): Positive integer representing the appointment ID.

    Request Body:
    - time (str, optional): The updated time for the appointment.
    - status (str, optional): The updated status for the appointment.

    Responses:
    - 200: Successful update of the appointment.
    - 404: Appointment not found.
    - 400: Invalid update state.
    """
    existing_appointment = run_query(
        """
    query ($id: Int!) {
        appointment(id: $id) {
            id
            user
            time
            status
        }
    }
    """,
        {"id": appointment_id},
    )

    if existing_appointment.get("data", {}).get("appointment") is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if update_data.status and update_data.status not in [
        "Scheduled",
        "Completed",
        "Cancelled",
    ]:
        raise HTTPException(status_code=400, detail="Invalid status transition")

    updated_data = {
        key: value for key, value in update_data.dict().items() if value is not None
    }

    # We assume that the transition is always valid when no status is being changed.
    if "status" in updated_data:
        if (
            existing_appointment["data"]["appointment"]["status"] == "Completed"
            and updated_data["status"] != "Completed"
        ):
            raise HTTPException(
                status_code=400, detail="Cannot change from Completed status"
            )

        if (
            existing_appointment["data"]["appointment"]["status"] == "Cancelled"
            and updated_data["status"] != "Cancelled"
        ):
            raise HTTPException(
                status_code=400, detail="Cannot change from Cancelled status"
            )

    update_appointment_data(appointment_id, updated_data)

    # Return the full updated appointment
    updated_appointment = run_query(
        """
    query ($id: Int!) {
        appointment(id: $id) {
            id
            user
            time
            status
        }
    }
    """,
        {"id": appointment_id},
    )

    return AppointmentResponse(**updated_appointment["data"]["appointment"])
