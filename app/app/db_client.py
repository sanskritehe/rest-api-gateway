from typing import List, Optional
import requests
from app.config import settings


def get_all_appointments() -> List[dict]:
    try:
        response = requests.get(f"{settings.DB_SERVICE_URL}/appointments")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch appointments from DB service: {str(e)}") from e


def get_appointment_by_id(appointment_id: int) -> Optional[dict]:
    try:
        response = requests.get(f"{settings.DB_SERVICE_URL}/appointments/{appointment_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch appointment from DB service: {str(e)}") from e


def delete_appointment(appointment_id: int) -> bool:
    try:
        response = requests.delete(f"{settings.DB_SERVICE_URL}/appointments/{appointment_id}")
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to delete appointment from DB service: {str(e)}") from e
