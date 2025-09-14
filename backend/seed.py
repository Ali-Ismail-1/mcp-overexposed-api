# backend/seed.py
from .db import Base, engine, SessionLocal
from .models import User


def seed() -> None:
	Base.metadata.create_all(bind=engine)
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


if __name__ == "__main__":
	seed()
