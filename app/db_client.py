from typing import Dict, Any, Optional

# Mock in-memory database storage for appointments
_appointments: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "user": "John Doe", "time": "2023-10-27T10:00:00", "status": "booked"},
    2: {"id": 2, "user": "Jane Smith", "time": "2023-10-27T11:00:00", "status": "pending"},
}

class DBClient:
    def get_appointment_by_id(self, appointment_id: int) -> Optional[Dict[str, Any]]:
        return _appointments.get(appointment_id)
