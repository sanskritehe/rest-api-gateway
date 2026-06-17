### FILE: app/db_client.py
```python
from typing import List, Optional
import requests
from app.config import settings


def get_all_appointments() -> List[dict]:
    try:
        response = requests.get(f"{settings.DB_SERVICE_URL}/appointments")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch appointments from DB service: {str(e)}") from e


def get_appointment_by_id(appointment_id: int) -> Optional[dict]:
    try:
        response = requests.get(f"{settings.DB_SERVICE_URL}/appointments/{appointment_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch appointment from DB service: {str(e)}") from e


def delete_appointment(appointment_id: int) -> bool:
    try:
        response = requests.delete(f"{settings.DB_SERVICE_URL}/appointments/{appointment_id}")
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to delete appointment from DB service: {str(e)}") from e
```

### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models import AppointmentResponse
from app.services.booking_service import list_appointments, delete_appointment_service

router = APIRouter(prefix="/appointments", tags=["Appointment"])


@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(booking_service=Depends(list_appointments)):
    try:
        appointments = booking_service()
        return appointments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve appointments: {str(e)}")


@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, delete_service=Depends(delete_appointment_service)):
    try:
        deleted = delete_service(appointment_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Appointment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete appointment: {str(e)}")
```

### FILE: app/services/booking_service.py
```python
from typing import List
from app.db_client import get_all_appointments, get_appointment_by_id, delete_appointment


def list_appointments() -> List[dict]:
    return get_all_appointments()


def delete_appointment_service(appointment_id: int) -> bool:
    existing_appointment = get_appointment_by_id(appointment_id)
    if not existing_appointment:
        return False
    return delete_appointment(appointment_id)
```

### FILE: tests/test_routes.py
```python
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_get_all_appointments_success():
    test_response = [
        {"id": 1, "user": "John Doe", "time": "2023-10-25T10:00:00", "status": "Scheduled"},
        {"id": 2, "user": "Jane Doe", "time": "2023-10-26T11:00:00", "status": "Scheduled"}
    ]
    with patch("app.services.booking_service.list_appointments", return_value=test_response):
        response = client.get("/appointments/")
        assert response.status_code == 200
        assert response.json() == test_response


def test_get_all_appointments_empty():
    with patch("app.services.booking_service.list_appointments", return_value=[]):
        response = client.get("/appointments/")
        assert response.status_code == 200
        assert response.json() == []


def test_delete_appointment_success():
    test_id = 1
    with patch("app.services.booking_service.delete_appointment_service", return_value=True):
        response = client.delete(f"/appointments/{test_id}")
        assert response.status_code == 204


def test_delete_appointment_not_found():
    test_id = 999
    with patch("app.services.booking_service.delete_appointment_service", return_value=False):
        response = client.delete(f"/appointments/{test_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Appointment not found"}
```