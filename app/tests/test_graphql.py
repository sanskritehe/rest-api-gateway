from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_microsoft_repos_success():
    query = """
    query {
        microsoftRepos {
            id
            name
            url
        }
    }
    """
    test_data = [
        {"id": 1, "name": "repo1", "html_url": "https://github.com/microsoft/repo1"},
        {"id": 2, "name": "repo2", "html_url": "https://github.com/microsoft/repo2"},
    ]
    with patch("app.services.github_service.list_microsoft_repos", return_value=test_data):
        response = client.post("/graphql", json={"query": query})
        assert response.status_code == 200
        assert "errors" not in response.json()
        data = response.json()["data"]["microsoftRepos"]
        expected_data = [
            {"id": 1, "name": "repo1", "url": "https://github.com/microsoft/repo1"},
            {"id": 2, "name": "repo2", "url": "https://github.com/microsoft/repo2"},
        ]
        assert data == expected_data
