from sqlalchemy import asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from db.models.patient import Patient
from db.note_repository import delete_notes_by_patient_id
from models.patient import PatientCreate, PatientResponse, PatientsResponse


async def get_all_patients(
    session: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    sort_by: str = "last_name",
    sort_order: str = "asc",
):
    offset = (page - 1) * page_size
    total = (await session.execute(select(func.count()).select_from(Patient))).scalar()
    if total is None:
        total = 0

    sort_column = getattr(Patient, sort_by, Patient.last_name)
    order = asc(sort_column) if sort_order == "asc" else desc(sort_column)

    patients = (
        (
            await session.execute(
                select(Patient)
                .order_by(order, Patient.id)
                .offset(offset)
                .limit(page_size)
            )
        )
        .scalars()
        .all()
    )

    patients = [PatientResponse.model_validate(p) for p in patients]
    return PatientsResponse(
        patients=patients,
        count_patients=total,
        current_page=page,
        page_size=page_size,
        total_pages=-(-total // page_size),
    )


async def get_patient_by_id(session: AsyncSession, id: int):
    my_patient = await session.get(Patient, id)

    if my_patient is None:
        return None

    my_patient = PatientResponse.model_validate(my_patient)

    return my_patient


async def create_patient(session: AsyncSession, new_patient: PatientCreate):
    insert_patient = Patient(
        first_name=new_patient.first_name,
        last_name=new_patient.last_name,
        dob=new_patient.dob,
    )
    session.add(insert_patient)
    await session.commit()
    await session.refresh(insert_patient)
    return insert_patient


async def update_patient(session: AsyncSession, patient_id: int, update: PatientCreate):
    existing = await session.get(Patient, patient_id)

    if existing is None:
        return None

    existing.first_name = update.first_name
    existing.last_name = update.last_name
    existing.dob = update.dob

    await session.commit()

    existing = PatientResponse.model_validate(existing)
    return existing


async def delete_patient_record(session: AsyncSession, patient_id: int):
    to_be_deleted = await session.get(Patient, patient_id)
    if to_be_deleted is None:
        return None

    await delete_notes_by_patient_id(session, patient_id)

    await session.delete(to_be_deleted)
    await session.commit()
    return to_be_deleted
