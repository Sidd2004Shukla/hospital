from pydantic import BaseModel, ConfigDict


class DoctorCreate(BaseModel):
    id: int | None = None
    name: str
    specialization: str


class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str

    model_config = ConfigDict(from_attributes=True)
