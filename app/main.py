from fastapi import FastAPI
from app.routes.appointments import router as appointments_router

app = FastAPI(title="Appointment Database Service")

app.include_router(appointments_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Appointment Database Service"}
