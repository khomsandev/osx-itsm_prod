import getpass
import sys

from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User


def create_admin():
    print("=" * 50)
    print(" IT SERVICE DESK - PRODUCTION ADMIN SETUP")
    print("=" * 50)

    username = input("Admin Username: ").strip()
    full_name = input("Full Name: ").strip()
    email = input("Email: ").strip() or None

    department = input("Department [IT]: ").strip() or "IT"
    job_position = (
        input("Job Position [System Administrator]: ").strip()
        or "System Administrator"
    )

    if not username or not full_name:
        print("ERROR: Username and Full Name are required.")
        return

    password = getpass.getpass("Admin Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")

    if password != confirm_password:
        print("ERROR: Passwords do not match.")
        return

    if len(password) < 12:
        print("ERROR: Password must be at least 12 characters.")
        return

    db = SessionLocal()

    try:
        existing = db.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()

        if existing:
            print(f"ERROR: Username '{username}' already exists.")
            return

        admin = User(
            username=username,
            password_hash=hash_password(password),
            full_name=full_name,
            email=email,
            role="ADMIN",
            is_active=True,
            department=department,
            job_position=job_position,
            must_change_password=False,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("\nSUCCESS: Production Admin created.")
        print(f"User ID  : {admin.id}")
        print(f"Username : {admin.username}")
        print(f"Full Name: {admin.full_name}")
        print(f"Role     : {admin.role}")
        print(f"Active   : {admin.is_active}")

    except Exception as e:
        db.rollback()
        print(f"\nERROR: Cannot create Admin: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
