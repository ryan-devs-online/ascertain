from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Form, HTTPException, Response
from sqlalchemy.orm import Session

from db.database import get_session, start_db
from db.note_repository import (
    create_note,
    delete_notes_by_patient_id,
    get_notes_by_patient_id,
)
from db.patient_repository import (
    create_patient,
    delete_patient_record,
    get_all_patients,
    get_patient_by_id,
    update_patient,
)
from models.patient import PatientCreate
from services.patient_service import get_summary


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init database
    start_db()
    yield
    # shut down db


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    """Healthcheck endpoint. Returns ok if the service is live."""
    return {"status": "ok"}


@app.get("/patients")
def get_patients(session: Session = Depends(get_session)):
    """Return all patients in the database along with information about them. This is a paginated endpoint.
    Sorted by last_name by default, but can also be sorted by first_name, or id"""
    return get_all_patients(session)


@app.get("/patients/{id}")
def get_patient(id: int, session: Session = Depends(get_session)):
    """Get a single patient by ID"""
    result = get_patient_by_id(session, id)

    if result is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return result


@app.post("/patients")
def post_patient(patient: PatientCreate, session: Session = Depends(get_session)):
    """Create a patient record."""
    result = create_patient(session, patient)

    if result is None:
        raise HTTPException(status_code=400, detail="Failed to create patient")
    return result


@app.put("/patients/{id}", status_code=200)
def put_patient(
    id: int, patient: PatientCreate, session: Session = Depends(get_session)
):
    """Update a patient's record."""
    result = update_patient(session, id, patient)

    if result is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return result


@app.delete("/patients/{id}", status_code=204)
def delete_patient(id: int, session: Session = Depends(get_session)):
    """Deletes the patient record as well as any associated notes."""
    result = delete_patient_record(session, id)
    if result is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return Response(status_code=204)


@app.post("/patients/{id}/notes")
def post_patient_note(
    id: int,
    content: str = Form(...),
    date: str = Form(None),
    session: Session = Depends(get_session),
):
    """Add a note to a patients file"""
    result = create_note(session, id, content, date)
    return result


@app.get("/patients/{id}/notes")
def get_patient_notes(id: int, session: Session = Depends(get_session)):
    """Return all notes that a patient has."""
    return get_notes_by_patient_id(session, id)


@app.delete("/patients/{id}/notes", status_code=204)
def delete_patient_notes(id: int, session: Session = Depends(get_session)):
    """Deletes all patients notes."""
    delete_notes_by_patient_id(session, id)
    return Response(status_code=204)


@app.get("/patients/{id}/summary")
def get_patient_summary(id: int, session: Session = Depends(get_session)):
    """Return a summary of the patient and their notes."""
    summary = get_summary(session, id)

    if summary is None:
        raise HTTPException(status_code=400, detail="Missing Patient Information")
    return summary
