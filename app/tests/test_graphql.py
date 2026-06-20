from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_appointment_by_id_success():
    query = """
    query($id: Int!) {
        appointmentById(id: $id) {
            id
            user
            time
            status
        }
    }
    """
    test_id = 1
    test_response = {
        "id": 1,
        "user": "John Doe",
        "time": "2023-10-25T10:00:00",
        "status": "Scheduled"
    }
    with patch("app.services.booking_service.get_appointment_by_id", return_value=test_response):
        response = client.post("/graphql", json={"query": query, "variables": {"id": test_id}})
        assert response.status_code == 200
        assert "errors" not in response.json()
        data = response.json()["data"]["appointmentById"]
        assert data == {
            "id": test_response["id"],
            "user": test_response["user"],
            "time": test_response["time"],
            "status": test_response["status"]
        }
        assert set(data.keys()) == {"id", "user", "time", "status"}
        # Ensure that the response matches the test data
        assert data["id"] == test_response["id"]
        assert data["user"] == test_response["user"]
        assert data["time"] == test_response["time"]
        assert data["status"] == test_response["status"]


def test_appointment_by_id_not_found():
    query = """
    query($id: Int!) {
        appointmentById(id: $id) {
            id
            user
            time
            status
        }
    }
    """
    test_id = 999
    with patch("app.services.booking_service.get_appointment_by_id", return_value=None):
        response = client.post("/graphql", json={"query": query, "variables": {"id": test_id}})
        assert response.status_code == 200
        assert "errors" in response.json()
        assert response.json()["errors"][0]["message"] == "Appointment not found"


def test_microsoft_repos_success():
    query = """
    query {
        microsoftRepos {
            id
            name
            html_url
            description
            language
        }
    }
    """
    test_response = [
        {
            "id": 1,
            "name": "repo1",
            "html_url": "https://github.com/microsoft/repo1",
            "description": "Test repository 1",
            "language": "Python"
        },
        {
            "id": 2,
            "name": "repo2",
            "html_url": "https://github.com/microsoft/repo2",
            "description": "Test repository 2",
            "language": "JavaScript"
        }
    ]
    with patch("app.services.github_service.list_microsoft_repos_service", return_value=test_response):
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        assert "errors" not in response.json()
        data = response.json()["data"]["microsoftRepos"]
        assert data == [
            {
                "id": repo["id"],
                "name": repo["name"],
                "html_url": repo["html_url"],
                "description": repo["description"],
                "language": repo["language"]
            }
            for repo in test_response
        ]

