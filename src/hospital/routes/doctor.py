from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from hospital.database import get_db
from hospital.models.doctor import Doctor
from hospital.schemas.doctor import DoctorCreate, DoctorResponse

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.post(
    "",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):  # noqa: B008
    if doctor.id is not None:
        existing = db.query(Doctor).filter(Doctor.id == doctor.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Doctor ID already exists")

    db_doctor = Doctor(**doctor.model_dump(exclude_none=True))
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@router.get("", response_model=list[DoctorResponse])
def get_all_doctors(db: Session = Depends(get_db)):  # noqa: B008
    return db.query(Doctor).all()


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):  # noqa: B008
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
