import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
db_url = os.getenv("DATABASE_URL")
print(f"DEBUG: DATABASE_URL = {db_url}")

if not db_url:
    print("ERROR: DATABASE_URL is empty!")
else:
    engine = create_engine(db_url)
    try:
        with engine.connect() as conn:
            count = conn.execute(text("SELECT count(*) FROM products")).scalar()
            print(f"DEBUG: Products count = {count}")
            
            # If count is 0, let is check selection_products
            sp_count = conn.execute(text("SELECT count(*) FROM selection_products")).scalar()
            print(f"DEBUG: SelectionProducts count = {sp_count}")
    except Exception as e:
        print(f"ERROR: {e}")
