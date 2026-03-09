from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from db.models.note import Note
from models.note import NoteResponse, NotesResponse


async def create_note(session: AsyncSession, patient_id: int, content: str, date):
    insert_note = Note(
        patient_id=patient_id,
        content=content,
        date=date or datetime.now(),
    )
    session.add(insert_note)
    await session.commit()
    await session.refresh(insert_note)
    return insert_note


async def get_notes_by_patient_id(
    session: AsyncSession,
    patient_id: int,
):

    total = (
        await session.execute(
            select(func.count()).select_from(Note).where(Note.patient_id == patient_id)
        )
    ).scalar()

    if total is None or total == 0:
        return None

    patient_notes = (
        (await session.execute(select(Note).where(Note.patient_id == patient_id)))
        .scalars()
        .all()
    )

    patient_notes = [NoteResponse.model_validate(n) for n in patient_notes]

    return NotesResponse(notes=patient_notes, count_notes=total)


async def delete_note(session: AsyncSession, note_id: int):
    to_be_deleted_note = await session.get(Note, note_id)

    if to_be_deleted_note is None:
        return None

    await session.delete(to_be_deleted_note)
    await session.commit()
    return to_be_deleted_note


async def delete_notes_by_patient_id(session: AsyncSession, patient_id: int):
    patient_notes = (
        (await session.execute(select(Note).where(Note.patient_id == patient_id)))
        .scalars()
        .all()
    )

    if not patient_notes:
        return None
    for note in patient_notes:
        await session.delete(note)
    await session.commit()
    return
