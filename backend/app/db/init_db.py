from sqlalchemy.orm import Session
from backend.app.db.session import engine, Base
from backend.app.models.entities import CareerRole
from backend.app.db.seed_data import CAREER_ROLES_SEED

def init_db(db: Session = None) -> None:
    """Create tables and seed initial career roles if not present."""
    Base.metadata.create_all(bind=engine)
    
    # Check if roles already exist
    from backend.app.db.session import SessionLocal
    local_db = db or SessionLocal()
    try:
        existing_count = local_db.query(CareerRole).count()
        if existing_count == 0:
            print("Seeding initial 8 career roles into database...")
            for role_data in CAREER_ROLES_SEED:
                role = CareerRole(**role_data)
                local_db.add(role)
            local_db.commit()
            print("Career roles seeded successfully!")
        else:
            print(f"Database already contains {existing_count} career roles. Skipping seed.")
    finally:
        if not db:
            local_db.close()

if __name__ == "__main__":
    init_db()
