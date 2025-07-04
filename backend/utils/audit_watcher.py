import threading
import time
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text, bindparam
from backend.logger import logger

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def process_audit_row(row):
    logger.info(
        f"Audit log - Table: {row['table_name']}, "
        f"Operation: {row['operation']}, "
        f"Changed columns: {row['changed_columns']}, "
        f"New values: {row['new_values']}"
    )
    print(
    f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
    f"Table: {row['table_name']}, "
    f"Operation: {row['operation']}, "
    f"Changed columns: {row['changed_columns']}, "
    f"New values: {row['new_values']}"
    )

def audit_log_watcher():
    logger.info("Starting audit log watcher background thread")
    while True:
        try:
            with SessionLocal() as db:
                result = db.execute(
                    text("SELECT * FROM audit_log ORDER BY changed_at ASC LIMIT 10")
                )
                rows = result.mappings().all()
                ids = []
                for row in rows:
                    process_audit_row(row)
                    ids.append(row["id"])
                if ids:
                    db.execute(
                    text("DELETE FROM audit_log WHERE id = ANY(:ids)").bindparams(bindparam('ids', expanding=True)),
                    {"ids": ids}
                    )
                db.commit()
        except Exception as e:
            logger.error(f"Error in audit_log_watcher: {e}")
        time.sleep(5)
