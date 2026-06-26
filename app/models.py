from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from app.database import Base, engine


class AppointmentDB(Base):
    __tablename__ = "appointments"

    id: int = Column(Integer, primary_key=True, index=True)  # type: ignore
    user: str = Column(String, index=True)  # type: ignore
    time: str = Column(String)  # type: ignore
    status: str = Column(String, default="Scheduled")  # type: ignore


# Ensure table exists in SQLite database
Base.metadata.create_all(bind=engine)


class AppointmentCreate(BaseModel):
    user: str
    time: str


class AppointmentUpdate(BaseModel):
    time: str | None = None  # Optional field
    status: str | None = None  # Optional field


class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: str
    status: str
