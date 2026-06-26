from typing import List, Optional, Dict, Any
import requests
from app.config import settings


def get_all_appointments() -> List[dict]:
    try:
        response = requests.get(f"{settings.DB_SERVICE_URL}/appointments")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(
            f"Failed to fetch appointments from DB service: {str(e)}"
        ) from e


def get_appointment_by_id(appointment_id: int) -> Optional[dict]:
    query = """
    query ($id: Int!) {
        appointment_record(id: $id) {
            id
            user
            time
            status
        }
    }
    """
    variables = {"id": appointment_id}
    try:
        response = requests.post(
            f"{settings.DB_SERVICE_URL}/graphql",
            json={"query": query, "variables": variables},
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json().get("data", {}).get("appointment_record")
    except requests.RequestException as e:
        raise RuntimeError(
            f"Failed to fetch appointment from DB service: {str(e)}"
        ) from e


def update_appointment_data(appointment_id: int, data: Dict[str, Any]) -> None:
    try:
        response = requests.put(
            f"{settings.DB_SERVICE_URL}/appointments/{appointment_id}", json=data
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(
            f"Failed to update appointment in DB service: {str(e)}"
        ) from e
