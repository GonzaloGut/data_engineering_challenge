from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database.database import Base

class HiredEmployee(Base):
    __tablename__ = "hired_employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False, index=True)

    department_id = Column(
        Integer, 
        ForeignKey("departments.id"),
        nullable=False,
        index=True
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False,
        index=True
    )

