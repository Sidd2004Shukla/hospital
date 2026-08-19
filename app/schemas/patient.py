from pydantic import BaseModel, ConfigDict


class PatientCreate(BaseModel):
    id: int | None = None
    name: str
    email: str
    phone: str


class PatientResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    model_config = ConfigDict(from_attributes=True)
