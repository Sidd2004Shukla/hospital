from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from hospital.database import get_db
from hospital.models.appointment import Appointment
from hospital.models.doctor import Doctor
from hospital.models.patient import Patient
from hospital.schemas.appointment import AppointmentCreate, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    if appointment.id is not None:
        existing_id = (
            db.query(Appointment).filter(Appointment.id == appointment.id).first()
        )
        if existing_id:
            raise HTTPException(status_code=400, detail="Appointment ID already exists")

    patient_exists = (
        db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    )
    doctor_exists = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()

    if not patient_exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not doctor_exists:
        raise HTTPException(status_code=404, detail="Doctor not found")

    overlapping = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.appointment_start < appointment.appointment_end,
            Appointment.appointment_end > appointment.appointment_start,
        )
        .first()
    )

    if overlapping:
        raise HTTPException(
            status_code=400,
            detail="Appointment overlaps with an existing one",
        )

    db_appointment = Appointment(**appointment.model_dump(exclude_none=True))
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.get("", response_model=list[AppointmentResponse])
def get_all_appointments(db: Session = Depends(get_db)):  # noqa: B008
    return db.query(Appointment).all()


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),  # noqa: B008
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
