from sqlalchemy import Column, Integer, String

from hospital.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)  # Manual ID (no auto-increment)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
