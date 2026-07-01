import strawberry
from app.database import SessionLocal
from app.models import AppointmentDB


@strawberry.type
class GraphQLErrorType(Exception):
    message: str


def resolve_appointment_record(id: int):
    db = SessionLocal()
    try:
        appointment = db.query(AppointmentDB).filter(AppointmentDB.id == id).first()  # type: ignore
        if not appointment:
            return None
        return appointment
    finally:
        db.close()
