### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, HTTPException, Path
from app.models import AppointmentResponse
from app.db_client import get_appointment_by_id, delete_appointment
from app.graphql_client import run_query

router = APIRouter(prefix="/appointments", tags=["Appointment"])


# Existing GET endpoint
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def read_appointment(
    appointment_id: int = Path(..., title="The ID of the appointment", gt=0),
):
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

    return AppointmentResponse(**existing_appointment["data"]["appointment"])


# Updated DELETE endpoint
@router.delete("/{appointment_id}")
def delete_appointment_endpoint(
    appointment_id: int = Path(..., title="The ID of the appointment", gt=0),
):
    appointment = get_appointment_by_id(appointment_id)

    if appointment is None:
        raise HTTPException(status_code=404, detail={"detail": "Appointment not found"})

    delete_appointment(appointment_id)

    return {
        "message": "Appointment deleted successfully",
        "appointment_id": appointment_id,
    }

```