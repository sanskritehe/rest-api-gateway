from fastapi import APIRouter, HTTPException, Depends, Path
from typing import List
from app.models import AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["Appointment"])


def get_list_service():
    import app.services.booking_service as booking_service
    return booking_service.list_appointments


def get_appointment_service():
    import app.services.booking_service as booking_service
    return booking_service.get_appointment_by_id


def get_delete_service():
    import app.services.booking_service as booking_service
    return booking_service.delete_appointment_service


@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(list_service=Depends(get_list_service)):
    try:
        appointments = list_service()
        return appointments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve appointments: {str(e)}")


@router.get("/{id}", response_model=AppointmentResponse)
def get_appointment(
    id: int = Path(..., title="The ID of the appointment to fetch", ge=1),
    appointment_service=Depends(get_appointment_service)
):
    """
    GET /appointments/{id}
    Fetches an appointment by ID.

    Path Parameters:
    - id (int): Positive integer representing the appointment ID.

    Responses:
    - 200: Successful retrieval.
    - 404: Appointment not found.
    - 500: Internal server error.
    """
    try:
        appointment = appointment_service(id)
        if appointment is None:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found",
            )
        return appointment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve appointment: {str(e)}")


@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(
    appointment_id: int = Path(..., title="The ID of the appointment to delete", ge=1),
    delete_service=Depends(get_delete_service),
):
    """
    DELETE /appointments/{appointment_id}
    Performs a hard delete of an appointment by ID.

    Path Parameters:
    - appointment_id (int): Positive integer representing the appointment ID.

    Responses:
    - 204: No Content on successful deletion.
    - 404: Appointment not found.
    - 500: Internal server error.
    """
    try:
        deleted = delete_service(appointment_id)
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail={"message": "Appointment not found", "code": "not_found"},
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete appointment: {str(e)}")
