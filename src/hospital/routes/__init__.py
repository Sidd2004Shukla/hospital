"""Routes package for hospital API."""

from hospital.routes.appointment import router as appointment_router
from hospital.routes.doctor import router as doctor_router
from hospital.routes.patient import router as patient_router

__all__ = ["patient_router", "doctor_router", "appointment_router"]
