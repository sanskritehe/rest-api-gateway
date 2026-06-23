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
