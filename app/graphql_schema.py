import strawberry
from typing import Optional
from app.database import SessionLocal
from app.models import AppointmentDB
from app.services.booking_service import (
    get_appointment_by_id as get_appointment_by_id_service,
)


@strawberry.type
class AppointmentStorage:
    id: int
    user: str
    time: str
    status: str


@strawberry.type
class Appointment:
    id: int
    patientName: str
    doctorName: str
    date: str
    status: str


@strawberry.type
class Query:
    @strawberry.field
    def appointment_record(self, id: int) -> Optional[AppointmentStorage]:
        db = SessionLocal()
        try:
            appointment = db.query(AppointmentDB).filter(AppointmentDB.id == id).first()  # type: ignore
            if appointment:
                return AppointmentStorage(
                    id=appointment.id,
                    user=appointment.user,
                    time=appointment.time,
                    status=appointment.status,
                )
            return None
        finally:
            db.close()

    @strawberry.field
    def appointment(self, id: int) -> Optional[Appointment]:
        appointment = get_appointment_by_id_service(appointment_id=id)
        if not appointment:
            return None
        return Appointment(
            id=appointment["id"],
            patientName=appointment["user"],  # Assuming user refers to patientName
            doctorName=appointment["doctorName"],  # Assuming need to extract doctorName
            date=appointment["time"],  # Assuming time refers to date
            status=appointment["status"],
        )


schema = strawberry.Schema(query=Query)
