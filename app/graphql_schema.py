from typing import Optional
from app.services.booking_service import get_appointment

class Query:
    def appointment(self, id: int) -> Optional[Appointment]:
        return get_appointment(id)
