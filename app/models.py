from sqlalchemy import Column, Integer, String
from app.database import Base

class AppointmentStorage(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)
    time = Column(String)
    status = Column(String)
