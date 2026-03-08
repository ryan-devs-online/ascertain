from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from db.models import patient


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey(patient.Patient.id))
    content: Mapped[str] = mapped_column(String)
    date: Mapped[date] = mapped_column(Date)
