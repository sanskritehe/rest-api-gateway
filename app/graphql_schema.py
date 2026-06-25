from typing import Optional
from app.models import AppointmentStorage
from app.services.booking_service import get_appointment
from sqlalchemy.orm import Session
from app.database import SessionLocal

class Query:
    def appointment_record(self, id: int) -> Optional[AppointmentStorage]:
        db: Session = SessionLocal()
        appointment = db.query(AppointmentStorage).filter(AppointmentStorage.id == id).first()
        return appointment
        
    def appointment(self, id: int) -> Optional[Appointment]:
        return get_appointment(id)

