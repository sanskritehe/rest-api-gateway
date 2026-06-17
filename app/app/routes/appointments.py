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
