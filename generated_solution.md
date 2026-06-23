### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, Path, HTTPException
from app.services.appointment_service import AppointmentService
from app.schemas.appointment import AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/{id:int}", response_model=AppointmentResponse)
def get_appointment(
    id: int = Path(..., gt=0, description="The ID of the appointment to retrieve."),
):
    """
    Get a single appointment by its ID.

    Arguments:
    - id: The ID of the appointment to retrieve.

    Returns:
    - The appointment details as a JSON response.
    """
    service = AppointmentService()
    appointment = service.get_appointment(id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return AppointmentResponse(**appointment)
```