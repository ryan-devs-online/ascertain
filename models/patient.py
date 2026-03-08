from datetime import date

from pydantic import BaseModel, ConfigDict


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    dob: date


class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    dob: date
    id: int


class PatientsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    count_patients: int
    current_page: int
    page_size: int
    total_pages: int
    patients: list[PatientResponse]
