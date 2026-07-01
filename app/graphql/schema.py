import strawberry
from app.graphql.resolvers import resolve_appointment_record
from typing import Optional


@strawberry.type
class AppointmentStorage:
    id: int
    user: str
    time: str
    status: str


@strawberry.type
class Query:
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

    @strawberry.field
    def getAppointment(self, id: int) -> Optional[AppointmentStorage]:
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
