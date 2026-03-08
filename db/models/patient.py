from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    dob: Mapped[date] = mapped_column(Date)

    def __repr__(self) -> str:
        return f"Patient(id={self.id!r}, first_name ={self.first_name!r}, last_name ={self.last_name!r}, dob ={self.dob!r})"
