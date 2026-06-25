from fastapi import FastAPI
from app.routes.appointments import router as appointments_router
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema

app = FastAPI(title="Appointment Service")

# Include Appointments routes
app.include_router(appointments_router)

# Include GraphQL router
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
