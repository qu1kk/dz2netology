from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class StudentGrade(Base):
    __tablename__ = "student_grades"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    last_name: Mapped[str] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(50))
    faculty: Mapped[str] = mapped_column(String(20))
    subject: Mapped[str] = mapped_column(String(100))
    grade: Mapped[int] = mapped_column(Integer)
