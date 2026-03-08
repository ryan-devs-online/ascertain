from pydantic import BaseModel, ConfigDict


class AISummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    patient_info: str
    patient_summary: str
