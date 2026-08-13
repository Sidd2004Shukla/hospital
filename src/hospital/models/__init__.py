"""Models package for hospital application."""

from hospital.models.appointment import Appointment
from hospital.models.doctor import Doctor
from hospital.models.patient import Patient

__all__ = ["Patient", "Doctor", "Appointment"]
