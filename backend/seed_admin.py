from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.user import User
from app.config.security import hash_password

def seed_admin():
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.email == "admin@scholartrack.com").first()
        if not admin:
            admin = User(
                name="System Admin",
                email="admin@scholartrack.com",
                password=hash_password("admin123"),
                role="ADMIN",
                verified_email=True
            )
            db.add(admin)
            db.commit()
            print("Admin user created successfully! (Email: admin@scholartrack.com / Password: admin123)")
        else:
            print("Admin already exists!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
