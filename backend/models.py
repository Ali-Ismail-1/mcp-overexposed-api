from sqlalchemy import Column, Integer, String, Date, JSON
from .db import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    work_email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    hire_date = Column(Date, nullable=True)
    salary = Column(Integer, nullable=True)
    manager_name = Column(String, nullable=True)

    # Extra blobs for demo
    leave = Column(JSON, nullable=True)
    emergency_contact = Column(JSON, nullable=True)
    payroll = Column(JSON, nullable=True)
    certifications = Column(JSON, nullable=True)  # could be list
