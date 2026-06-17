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
