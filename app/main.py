from fastapi import FastAPI
from app.routes import appointments
from app.database import SessionLocal

app = FastAPI()

app.include_router(appointments.router)
