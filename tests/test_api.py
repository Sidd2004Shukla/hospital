from fastapi.testclient import TestClient
from hospital.database import Base, get_db
from hospital.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import pytest

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)




def test_create_patient():
    response = client.post(
        "/patients",
        json={"id": 1, "name": "Alice", "email": "alice@example.com", "phone": "123"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"


def test_create_patient_duplicate_id():
    client.post(
        "/patients",
        json={"id": 1, "name": "Alice", "email": "alice@example.com", "phone": "123"},
    )
    response = client.post(
        "/patients",
        json={"id": 1, "name": "Bob", "email": "bob@example.com", "phone": "456"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Patient ID already exists"


def test_get_all_patients():
    client.post(
        "/patients",
        json={"id": 1, "name": "Alice", "email": "alice@example.com", "phone": "123"},
    )
    response = client.get("/patients")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_patient_by_id():
    client.post(
        "/patients",
        json={"id": 1, "name": "Alice", "email": "alice@example.com", "phone": "123"},
    )
    response = client.get("/patients/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_get_patient_not_found():
    response = client.get("/patients/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"




def test_create_doctor():
    response = client.post(
        "/doctors", json={"id": 1, "name": "Dr. Bob", "specialization": "General"}
    )
    assert response.status_code == 201


def test_create_doctor_duplicate_id():
    client.post(
        "/doctors", json={"id": 1, "name": "Dr. Bob", "specialization": "General"}
    )
    response = client.post(
        "/doctors", json={"id": 1, "name": "Dr. Smith", "specialization": "Surgery"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Doctor ID already exists"


def test_get_all_doctors():
    client.post(
        "/doctors", json={"id": 1, "name": "Dr. Bob", "specialization": "General"}
    )
    response = client.get("/doctors")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_doctor_by_id():
    client.post(
        "/doctors", json={"id": 1, "name": "Dr. Bob", "specialization": "General"}
    )
    response = client.get("/doctors/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Dr. Bob"


def test_get_doctor_not_found():
    response = client.get("/doctors/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Doctor not found"





def test_appointment_and_overlap_rule():
    client.post(
        "/patients",
        json={"id": 1, "name": "Alice", "email": "alice@example.com", "phone": "123"},
    )
    client.post(
        "/doctors", json={"id": 1, "name": "Dr. Bob", "specialization": "General"}
    )

    valid_res = client.post(
        "/appointments",
        json={
            "id": 1,
            "patient_id": 1,
            "doctor_id": 1,
            "appointment_start": "2026-08-15T10:00:00",
            "appointment_end": "2026-08-15T11:00:00",
        },
    )
    assert valid_res.status_code == 201

    overlap_res = client.post(
        "/appointments",
        json={
            "id": 2,
            "patient_id": 1,
            "doctor_id": 1,
            "appointment_start": "2026-08-15T10:30:00",
            "appointment_end": "2026-08-15T11:30:00",
        },
    )
    assert overlap_res.status_code == 400
    assert "overlaps" in overlap_res.json()["detail"]


def test_create_appointment_missing_patient_or_doctor():
    res = client.post(
        "/appointments",
        json={
            "id": 1,
            "patient_id": 999,
            "doctor_id": 999,
            "appointment_start": "2026-08-15T12:00:00",
            "appointment_end": "2026-08-15T13:00:00",
        },
    )
    assert res.status_code == 404


def test_get_all_appointments():
    client.post(
        "/patients", json={"id": 1, "name": "Alice", "email": "a@ex.com", "phone": "1"}
    )
    client.post("/doctors", json={"id": 1, "name": "Dr. Bob", "specialization": "Gen"})
    client.post(
        "/appointments",
        json={
            "id": 1,
            "patient_id": 1,
            "doctor_id": 1,
            "appointment_start": "2026-08-15T10:00:00",
            "appointment_end": "2026-08-15T11:00:00",
        },
    )

    response = client.get("/appointments")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_appointment_by_id():
    client.post(
        "/patients", json={"id": 1, "name": "Alice", "email": "a@ex.com", "phone": "1"}
    )
    client.post("/doctors", json={"id": 1, "name": "Dr. Bob", "specialization": "Gen"})
    client.post(
        "/appointments",
        json={
            "id": 1,
            "patient_id": 1,
            "doctor_id": 1,
            "appointment_start": "2026-08-15T10:00:00",
            "appointment_end": "2026-08-15T11:00:00",
        },
    )

    response = client.get("/appointments/1")
    assert response.status_code == 200


def test_get_appointment_not_found():
    response = client.get("/appointments/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Appointment not found"


def test_create_appointment_duplicate_id():
    
    client.post(
        "/patients", json={"id": 1, "name": "Alice", "email": "a@ex.com", "phone": "1"}
    )
    client.post("/doctors", json={"id": 1, "name": "Dr. Bob", "specialization": "Gen"})

    client.post(
        "/appointments",
        json={
            "id": 1,
            "patient_id": 1,
            "doctor_id": 1,
            "appointment_start": "2026-08-15T10:00:00",
            "appointment_end": "2026-08-15T11:00:00",
        },
    )

    res = client.post(
        "/appointments",
        json={
            "id": 1,
            "patient_id": 1,
            "doctor_id": 1,
            "appointment_start": "2026-08-16T10:00:00",
            "appointment_end": "2026-08-16T11:00:00",
        },
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "Appointment ID already exists"


def test_create_appointment_missing_doctor_only():
    client.post(
        "/patients", json={"id": 1, "name": "Alice", "email": "a@ex.com", "phone": "1"}
    )

    res = client.post(
        "/appointments",
        json={
            "id": 1,
            "patient_id": 1,
            "doctor_id": 999,
            "appointment_start": "2026-08-15T12:00:00",
            "appointment_end": "2026-08-15T13:00:00",
        },
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Doctor not found"
