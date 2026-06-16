### FILE: app/graphql/resolvers.py
```python
import strawberry
from app.services.github_service import list_microsoft_repos


@strawberry.field(name="microsoftRepos")
def resolve_microsoft_repos():
    return list_microsoft_repos()
```

### FILE: app/graphql/schema.py
```python
import strawberry
from app.graphql.resolvers import resolve_microsoft_repos

@strawberry.type
class MicrosoftRepo:
    id: int
    name: str
    url: str

@strawberry.type
class Query:
    @strawberry.field
    def microsoft_repos(self) -> list[MicrosoftRepo]:
        raw_repos = resolve_microsoft_repos()
        return [
            MicrosoftRepo(
                id=repo["id"],
                name=repo["name"],
                url=repo["html_url"]
            )
            for repo in raw_repos
        ]

schema = strawberry.Schema(query=Query)
```

### FILE: app/main.py
```python
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema

app = FastAPI(title="GraphQL Service")

# Add GraphQL endpoint
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
```

### FILE: app/services/github_service.py
```python
from app.db_client import get_microsoft_repos


def list_microsoft_repos():
    return get_microsoft_repos()
```

### FILE: tests/test_graphql.py
```python
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
```