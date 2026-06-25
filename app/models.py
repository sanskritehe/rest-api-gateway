from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from app.database import Base, engine

class AppointmentDB(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)
    time = Column(String)
    status = Column(String, default="Scheduled")

# Ensure table exists in SQLite database
Base.metadata.create_all(bind=engine)

class AppointmentCreate(BaseModel):
    user: str
    time: str

class AppointmentUpdate(BaseModel):
    time: str

class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: str
    status: str
