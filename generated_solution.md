### FILE: app/config.py
```python
from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    DB_SERVICE_URL: HttpUrl = "http://localhost:8001"


settings = Settings()
```

### FILE: app/db_client.py
```python
from typing import List
import requests
from app.config import settings


def get_all_appointments() -> List[dict]:
    try:
        response = requests.get(f"{settings.DB_SERVICE_URL}/appointments")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch appointments from DB service: {str(e)}") from e
```

### FILE: app/main.py
```python
from fastapi import FastAPI
from app.routes.appointments import router as appointments_router

app = FastAPI(title="Appointment Service")

# Include Appointments routes
app.include_router(appointments_router)
```

### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models import AppointmentResponse
from app.services.booking_service import list_appointments

router = APIRouter(prefix="/appointments", tags=["Appointment"])


@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(booking_service=Depends(list_appointments)):
    try:
        appointments = booking_service()
        return appointments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve appointments: {str(e)}")
```

### FILE: app/services/booking_service.py
```python
from typing import List
from app.db_client import get_all_appointments


def list_appointments() -> List[dict]:
    return get_all_appointments()
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
```