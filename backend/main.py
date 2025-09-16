# backend/main.py
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from datetime import date

from .db import Base, engine, get_db, SessionLocal
from .models import Employee

app = FastAPI(title="Overexposed Employees Demo")
router = APIRouter(prefix="/api")

# -------------------------
# Pydantic Models
# -------------------------

class EmployeeListOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    work_email: str
    model_config = ConfigDict(from_attributes=True)


class EmployeeDetailOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    hire_date: date
    manager_name: str
    model_config = ConfigDict(from_attributes=True)


class LeaveOut(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    notes: str
    model_config = ConfigDict(from_attributes=True)


class EmergencyContactOut(BaseModel):
    name: str
    relationship: str
    phone: str
    address: str
    model_config = ConfigDict(from_attributes=True)


class PayrollOut(BaseModel):
    salary: int
    pay_period_start: date
    pay_period_end: date
    deposit_account_last4: str
    model_config = ConfigDict(from_attributes=True)


class CertificationOut(BaseModel):
    cert_name: str
    issued_date: date
    expiry_date: date
    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Startup: create + seed DB
# -------------------------

@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Employee).first() is None:
            sample_employees = [
				{
					"first_name": "Alice",
					"last_name": "Smith",
					"work_email": "alice.smith@company.com",
					"phone": "555-111-2222",
					"address": "123 Main St, Springfield",
					# REAL Date fields → keep as Python date
					"birthday": date(1990, 5, 12),
					"hire_date": date(2015, 6, 1),
					"salary": 120000,
					"manager_name": "Bob Johnson",
					# JSON fields → dates must be strings
					"leave": {
						"leave_type": "Medical",
						"start_date": date(2023, 5, 10).isoformat(),
						"end_date": date(2023, 5, 12).isoformat(),
						"notes": "Doctor appointment, annual physical (DOB: 05/12/1990)",
					},
					"emergency_contact": {
						"name": "Jane Smith",
						"relationship": "Spouse",
						"phone": "555-999-8888",
						"address": "123 Main St, Springfield",
					},
					"payroll": {
						"salary": 120000,
						"pay_period_start": date(2023, 5, 1).isoformat(),
						"pay_period_end": date(2023, 5, 15).isoformat(),
						"deposit_account_last4": "1234",
					},
					"certifications": [
						{
							"cert_name": "Security Awareness",
							"issued_date": date(2022, 1, 1).isoformat(),
							"expiry_date": date(2024, 1, 1).isoformat(),
						},
					],
				},
				{
					"first_name": "Bob",
					"last_name": "Johnson",
					"work_email": "bob.johnson@company.com",
					"phone": "555-333-4444",
					"address": "456 Oak Ave, Springfield",
					# REAL Date fields
					"birthday": date(1985, 9, 23),
					"hire_date": date(2010, 3, 15),
					"salary": 150000,
					"manager_name": "Carol Danvers",
					# JSON fields
					"leave": {
						"leave_type": "Vacation",
						"start_date": date(2023, 7, 1).isoformat(),
						"end_date": date(2023, 7, 15).isoformat(),
						"notes": "Family vacation",
					},
					"emergency_contact": {
						"name": "Mike Johnson",
						"relationship": "Brother",
						"phone": "555-222-1111",
						"address": "456 Oak Ave, Springfield",
					},
					"payroll": {
						"salary": 150000,
						"pay_period_start": date(2023, 5, 1).isoformat(),
						"pay_period_end": date(2023, 5, 15).isoformat(),
						"deposit_account_last4": "5678",
					},
					"certifications": [
						{
							"cert_name": "Leadership Training",
							"issued_date": date(2021, 6, 1).isoformat(),
							"expiry_date": date(2023, 6, 1).isoformat(),
						},
					],
				},
			]

            for e in sample_employees:
                db.add(Employee(**e))
            db.commit()
    finally:
        db.close()

# -------------------------
# Routes
# -------------------------

@router.get("/employees", response_model=list[EmployeeListOut])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@router.get("/employees/{employee_id}", response_model=EmployeeDetailOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.get("/employees/{employee_id}/leave", response_model=LeaveOut)
def get_leave(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee or not employee.leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return employee.leave

@router.get("/employees/{employee_id}/emergency-contact", response_model=EmergencyContactOut)
def get_emergency_contact(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee or not employee.emergency_contact:
        raise HTTPException(status_code=404, detail="Emergency contact not found")
    return employee.emergency_contact

@router.get("/employees/{employee_id}/payroll", response_model=PayrollOut)
def get_payroll(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee or not employee.payroll:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return employee.payroll

@router.get("/employees/{employee_id}/certifications", response_model=list[CertificationOut])
def get_certifications(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee or not employee.certifications:
        raise HTTPException(status_code=404, detail="Certifications not found")
    return employee.certifications

app.include_router(router)
