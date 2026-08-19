"""Routes package for hospital API."""

from app.routes.appointment import router as appointment_router
from app.routes.doctor import router as doctor_router
from app.routes.patient import router as patient_router

__all__ = ["appointment_router", "doctor_router", "patient_router"]
