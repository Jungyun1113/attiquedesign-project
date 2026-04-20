from sqlmodel import Session, text
from chalicelib.core.db import get_engine

def migrate():
    engine = get_engine()
    with Session(engine) as session:
        print("Checking for sort_order column in selections table...")
        try:
            # PostgreSQL syntax to add column if not exists
            session.execute(text("ALTER TABLE selections ADD COLUMN IF NOT EXISTS sort_order INTEGER DEFAULT 0"))
            session.commit()
            print("Successfully added sort_order column (or it already existed).")
        except Exception as e:
            print(f"Error migrating: {e}")
            session.rollback()

if __name__ == "__main__":
    migrate()
