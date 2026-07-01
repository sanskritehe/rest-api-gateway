import strawberry
from typing import Optional
from app.services.booking_service import (
    get_appointment_by_id as get_appointment_by_id_service,
)


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
    def appointment(self, id: int) -> Optional[Appointment]:
        appointment = get_appointment_by_id_service(appointment_id=id)
        if not appointment:
            raise Exception("Appointment not found")
        return Appointment(
            id=appointment["id"],
            patientName=appointment["patientName"],
            doctorName=appointment["doctorName"],
            date=appointment["date"],
            status=appointment["status"],
        )


schema = strawberry.Schema(query=Query)
