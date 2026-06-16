from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_get_appointment_by_id_success():
    test_id = 1
    test_data = {
        "id": test_id,
        "user": "John Doe",
        "time": "2023-10-25T10:00:00",
        "status": "Scheduled"
    }
    with patch("app.services.booking_service.get_appointment_by_id", return_value=test_data):
        response = client.get(f"/appointments/{test_id}")
        assert response.status_code == 200
        assert response.json() == test_data

def test_get_appointment_by_id_not_found():
    test_id = 9999
    with patch("app.services.booking_service.get_appointment_by_id", return_value=None):
        response = client.get(f"/appointments/{test_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Appointment not found"}

def test_get_appointment_by_id_invalid_id():
    test_id = -1  # Invalid ID
    response = client.get(f"/appointments/{test_id}")
    assert response.status_code == 422  # FastAPI will automatically raise 422 for invalid path params
