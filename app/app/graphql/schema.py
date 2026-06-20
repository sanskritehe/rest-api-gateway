import strawberry
from app.graphql.resolvers import resolve_appointment_by_id, resolve_microsoft_repos

@strawberry.type
class Appointment:
    id: int
    user: str
    time: str
    status: str

@strawberry.type
class Repository:
    id: int
    name: str
    html_url: str
    description: str
    language: str

@strawberry.type
class Query:
    @strawberry.field
    def appointmentById(self, id: int) -> Appointment:
        appointment = resolve_appointment_by_id(id=id)
        return Appointment(
            id=appointment["id"],
            user=appointment["user"],
            time=appointment["time"],
            status=appointment["status"]
        )
    
    @strawberry.field
    def microsoftRepos(self) -> list[Repository]:
        repos = resolve_microsoft_repos()
        return [
            Repository(
                id=repo["id"],
                name=repo["name"],
                html_url=repo["html_url"],
                description=repo["description"],
                language=repo["language"]
            )
            for repo in repos
        ]

schema = strawberry.Schema(query=Query)
