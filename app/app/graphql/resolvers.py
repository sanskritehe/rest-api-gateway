import strawberry
from app.services.github_service import list_microsoft_repos


@strawberry.field(name="microsoftRepos")
def resolve_microsoft_repos():
    return list_microsoft_repos()
