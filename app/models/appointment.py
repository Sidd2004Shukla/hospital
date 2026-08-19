from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)  # Manual ID (no auto-increment)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_start = Column(DateTime, nullable=False)
    appointment_end = Column(DateTime, nullable=False)

    patient = relationship("Patient")
    doctor = relationship("Doctor")
