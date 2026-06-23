### FILE: app/db_client.py
```python
from typing import Dict, Any, Optional

# Mock in-memory database storage for appointments
_appointments: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "user": "John Doe", "time": "2023-10-27T10:00:00", "status": "booked"},
    2: {"id": 2, "user": "Jane Smith", "time": "2023-10-27T11:00:00", "status": "pending"},
}

class DBClient:
    def get_appointment_by_id(self, appointment_id: int) -> Optional[Dict[str, Any]]:
        return _appointments.get(appointment_id)
```

### FILE: app/services/appointment_service.py
```python
from typing import Optional, Dict, Any
from app.db_client import DBClient

class AppointmentService:
    def __init__(self, db_client: Optional[DBClient] = None):
        self.db_client = db_client or DBClient()

    def get_appointment(self, appointment_id: int) -> Optional[Dict[str, Any]]:
        return self.db_client.get_appointment_by_id(appointment_id)
```

### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["appointments"])

class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: str
    status: str

def get_appointment_service() -> AppointmentService:
    return AppointmentService()

@router.get("/{id}", response_model=AppointmentResponse, status_code=status.HTTP_200_OK)
def get_appointment(id: int, service: AppointmentService = Depends(get_appointment_service)):
    appointment = service.get_appointment(id)
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with ID {id} not found"
        )
    return appointment
```

### FILE: app/main.py
```python
from fastapi import FastAPI
from app.routes.appointments import router as appointments_router

app = FastAPI(title="Appointment Database Service")

app.include_router(appointments_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Appointment Database Service"}
```