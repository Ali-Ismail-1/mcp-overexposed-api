# backend/main.py
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from .db import Base, engine, get_db, SessionLocal
from .models import User

app = FastAPI(title="Overexposed Data Demo")
router = APIRouter(prefix="/api")


class UserOutAll(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	id: int
	name: str
	email: str
	ssn: str
	salary: int


class UserPublicOut(BaseModel):
	first_name: str


@app.on_event("startup")
def on_startup() -> None:
	# Create tables
	Base.metadata.create_all(bind=engine)

	# Seed sample data if empty
	db = SessionLocal()
	try:
		any_user = db.query(User).first()
		if any_user is None:
			sample_users = [
				{"name": "Alice Smith", "email": "alice@example.com", "ssn": "123-45-6789", "salary": 120000},
				{"name": "Bob Johnson", "email": "bob@example.com", "ssn": "987-65-4321", "salary": 95000},
				{"name": "Carol Danvers", "email": "carol@example.com", "ssn": "555-12-3456", "salary": 150000},
			]
			for u in sample_users:
				db.add(User(**u))
			db.commit()
	finally:
		db.close()


@router.get("/users/{user_id}", response_model=UserOutAll)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserOutAll:
	user = db.query(User).filter(User.id == user_id).first()
	if user is None:
		raise HTTPException(status_code=404, detail="User not found")
	return UserOutAll.model_validate(user)


@router.get("/users/{user_id}/public", response_model=UserPublicOut)
def get_user_public(user_id: int, db: Session = Depends(get_db)) -> UserPublicOut:
	user = db.query(User).filter(User.id == user_id).first()
	if user is None:
		raise HTTPException(status_code=404, detail="User not found")
	first_name = user.name.split()[0] if user.name else ""
	return UserPublicOut(first_name=first_name)


app.include_router(router)
