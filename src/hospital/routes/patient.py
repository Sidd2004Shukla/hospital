from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from hospital.database import get_db
from hospital.models.patient import Patient
from hospital.schemas.patient import PatientCreate, PatientResponse

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):  # noqa: B008
    if patient.id is not None:
        existing = db.query(Patient).filter(Patient.id == patient.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Patient ID already exists")

    db_patient = Patient(**patient.model_dump(exclude_none=True))
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.get("", response_model=list[PatientResponse])
def get_all_patients(db: Session = Depends(get_db)):  # noqa: B008
    return db.query(Patient).all()


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):  # noqa: B008
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
