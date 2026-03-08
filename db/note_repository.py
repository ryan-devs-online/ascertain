from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from db.models.note import Note
from models.note import NoteResponse, NotesResponse


def create_note(session: Session, patient_id: int, content: str, date):
    insert_note = Note(
        patient_id=patient_id,
        content=content,
        date=date or datetime.now(),
    )
    session.add(insert_note)
    session.commit()
    session.refresh(insert_note)
    return insert_note


def get_note_by_note_id(session: Session, note_id: int):
    my_note = session.get(Note, note_id)

    my_note = NoteResponse.model_validate(my_note)

    return my_note


def get_notes_by_patient_id(
    session: Session,
    patient_id: int,
):

    total = session.execute(
        select(func.count()).select_from(Note).where(Note.patient_id == patient_id)
    ).scalar()

    if total is None:
        total = 0

    patient_notes = (
        session.execute(select(Note).where(Note.patient_id == patient_id))
        .scalars()
        .all()
    )

    patient_notes = [NoteResponse.model_validate(n) for n in patient_notes]

    return NotesResponse(notes=patient_notes, count_notes=total)


def delete_note(session: Session, note_id: int):
    to_be_deleted_note = session.get(Note, note_id)

    if to_be_deleted_note is None:
        return None

    session.delete(to_be_deleted_note)
    session.commit()
    return to_be_deleted_note


def delete_notes_by_patient_id(session: Session, patient_id: int):
    patient_notes = (
        session.execute(select(Note).where(Note.patient_id == patient_id))
        .scalars()
        .all()
    )

    if not patient_notes:
        return None
    for note in patient_notes:
        session.delete(note)
    session.commit()
    return
