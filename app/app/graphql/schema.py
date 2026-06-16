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
