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
    """
    Fetch the data from the Database Service using GraphQL.
    Fallback to REST if GraphQL fails or if not available.
    """
    query = """
    query GetAppointmentRecord($id: Int!) {
        appointment_record(id: $id) {
            id
            user
            time
            status
        }
    }
    """
    try:
        response = requests.post(
            f"{settings.DB_SERVICE_URL}/graphql",
            json={"query": query, "variables": {"id": appointment_id}},
            timeout=5
        )
        if response.status_code == 200:
            res_json = response.json()
            if "errors" not in res_json or not res_json["errors"]:
                data = res_json.get("data")
                if data and data.get("appointment_record"):
                    return data["appointment_record"]
    except Exception:
        pass

    # REST Fallback
    try:
        response = requests.get(f"{settings.DB_SERVICE_URL}/appointments/{appointment_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch appointment from DB service: {str(e)}") from e


def delete_appointment(appointment_id: int) -> bool:
    """
    Perform a hard delete of the appointment record from the database.

    Args:
        appointment_id (int): ID of the appointment to be deleted.

    Returns:
        bool: True if the record was successfully deleted, False if not found.
    """
    try:
        response = requests.delete(f"{settings.DB_SERVICE_URL}/appointments/{appointment_id}")
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to delete appointment from DB service: {str(e)}") from e


def get_microsoft_repos() -> List[dict]:
    """
    Fetch the public repositories from Microsoft's GitHub organization.

    Returns:
        List[dict]: A list of repositories.
    """
    try:
        response = requests.get("https://api.github.com/orgs/microsoft/repos")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch Microsoft repositories: {str(e)}") from e
