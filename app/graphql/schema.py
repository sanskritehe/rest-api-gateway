import strawberry
from app.graphql.resolvers import (
    resolve_appointment_by_id,
    resolve_appointment_record,
)
from typing import Optional


@strawberry.type
class Appointment:
    id: int
    user: str
    time: str
    status: str


@strawberry.type
class AppointmentStorage:
    id: int
    user: str
    time: str
    status: str


@strawberry.type
class Query:
    @strawberry.field
    def appointmentById(self, id: int) -> Optional[Appointment]:
        appointment = resolve_appointment_by_id(id=id)
        return Appointment(
            id=appointment["id"],
            user=appointment["user"],
            time=appointment["time"],
            status=appointment["status"],
        )

    @strawberry.field
    def appointment(self, id: int) -> Optional[Appointment]:
        appointment = resolve_appointment_by_id(id=id)
        return Appointment(
            id=appointment["id"],
            user=appointment["user"],
            time=appointment["time"],
            status=appointment["status"],
        )

    @strawberry.field
    def appointment_record(self, id: int) -> Optional[AppointmentStorage]:
        appointment = resolve_appointment_record(id=id)
        if not appointment:
            return None
        return AppointmentStorage(
            id=appointment.id,
            user=appointment.user,
            time=appointment.time,
            status=appointment.status,
        )


schema = strawberry.Schema(query=Query)
