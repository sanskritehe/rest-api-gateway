from typing import List
from app.db_client import get_all_appointments


def list_appointments() -> List[dict]:
    return get_all_appointments()
