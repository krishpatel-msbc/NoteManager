import threading
import time
import os
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from backend.logger import logger
from backend.core.config import settings

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

API_URL = settings.API_URL

def api_call_worker():
    logger.info("Starting API call watcher thread")
    while True:
        try:
            with SessionLocal() as db:
                result = db.execute(
                    text("SELECT * FROM api_call_queue ORDER BY created_at ASC LIMIT 10")
                    )
                rows = result.mappings().all()
                ids = []
                for row in rows:
                    try:
                        resp = requests.post(API_URL, json={
                            "table": row["table_name"],
                            "operation": row["operation"],
                            "changes": row["new_values"],
                            "columns": row["changed_columns"]
                        })
                        resp.raise_for_status()
                        logger.info(f"Sent API call: {resp.status_code}")
                        ids.append(row["id"])
                    except Exception as e:
                        logger.error(f"API call failed: {e}")
                if ids:
                    db.execute(
                        text("DELETE FROM api_call_queue WHERE id = ANY(:ids)"),
                        {"ids": ids}
                    )
                    db.commit()
        except Exception as e:
            logger.error(f"Error in api_call_worker: {e}")
        time.sleep(5)