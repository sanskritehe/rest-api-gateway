import strawberry
from typing import Optional
from app.services.booking_service import get_appointment_by_id as get_appointment_by_id_service
from app.database import SessionLocal

@strawberry.type
class AppointmentStorage:
    id: int
    user: str
    time: str
    status: str

@strawberry.type
class Appointment:
    id: int
    user: str
    time: str
    status: str

@strawberry.type
class Query:
    @strawberry.field
    def appointment_record(self, id: int) -> Optional[AppointmentStorage]:
        db = SessionLocal()
        try:
            from sqlalchemy import text
            try:
                result = db.execute(
                    text("SELECT id, user, time, status FROM appointments WHERE id = :id"),
                    {"id": id}
                ).fetchone()
                if result:
                    return AppointmentStorage(
                        id=result[0],
                        user=result[1],
                        time=result[2],
                        status=result[3]
                    )
            except Exception:
                pass
            
            appointment = get_appointment_by_id_service(appointment_id=id)
            if appointment:
                return AppointmentStorage(
                    id=appointment["id"],
                    user=appointment["user"],
                    time=appointment["time"],
                    status=appointment["status"]
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
            user=appointment["user"],
            time=appointment["time"],
            status=appointment["status"]
        )
    
    @strawberry.field
    def appointmentById(self, id: int) -> Optional[Appointment]:
        appointment = get_appointment_by_id_service(appointment_id=id)
        if not appointment:
            return None
        return Appointment(
            id=appointment["id"],
            user=appointment["user"],
            time=appointment["time"],
            status=appointment["status"]
        )

schema = strawberry.Schema(query=Query)
