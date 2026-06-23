from typing import Optional, Dict, Any
from app.db_client import DBClient

class AppointmentService:
    def __init__(self, db_client: Optional[DBClient] = None):
        self.db_client = db_client or DBClient()

    def get_appointment(self, appointment_id: int) -> Optional[Dict[str, Any]]:
        return self.db_client.get_appointment_by_id(appointment_id)
