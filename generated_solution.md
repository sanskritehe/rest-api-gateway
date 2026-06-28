### FILE: app/routes/appointments.py
```python
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
```

### FILE: app/services/booking_service.py
```python
from typing import List, Optional
from app.db_client import (
    get_all_appointments,
    get_appointment_by_id as db_get_appointment_by_id,
    delete_appointment_by_id as db_delete_appointment_by_id,
)


def list_appointments() -> List[dict]:
    return get_all_appointments()


def get_appointment_by_id(appointment_id: int) -> Optional[dict]:
    return db_get_appointment_by_id(appointment_id)


def delete_appointment_by_id(appointment_id: int) -> Optional[dict]:
    return db_delete_appointment_by_id(appointment_id)
```

### FILE: app/db_client.py
```python
from typing import List, Optional, Dict, Any
import requests
from app.config import settings


def get_all_appointments() -> List[dict]:
    try:
        response = requests.get(f"{settings.DB_SERVICE_URL}/appointments")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(
            f"Failed to fetch appointments from DB service: {str(e)}"
        ) from e


def get_appointment_by_id(appointment_id: int) -> Optional[dict]:
    query = """
    query ($id: Int!) {
        appointment_record(id: $id) {
            id
            user
            time
            status
        }
    }
    """
    variables = {"id": appointment_id}
    try:
        response = requests.post(
            f"{settings.DB_SERVICE_URL}/graphql",
            json={"query": query, "variables": variables},
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json().get("data", {}).get("appointment_record")
    except requests.RequestException as e:
        raise RuntimeError(
            f"Failed to fetch appointment from DB service: {str(e)}"
        ) from e


def delete_appointment_by_id(appointment_id: int) -> Optional[dict]:
    try:
        response = requests.delete(
            f"{settings.DB_SERVICE_URL}/appointments/{appointment_id}"
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(
            f"Failed to delete appointment in DB service: {str(e)}"
        ) from e
```