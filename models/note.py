from datetime import date

from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    content: str
    date: date


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    content: str
    date: date


class NotesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    count_notes: int
    notes: list[NoteResponse]
