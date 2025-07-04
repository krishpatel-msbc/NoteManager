import threading
import time
import os
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from backend.logger import logger
from backend.core.config import settings

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize SQLAlchemy engine and session maker
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# API URL to which requests will be sent
API_URL = settings.API_URL

def api_call_worker():
    """
    Background worker function that:
    - Periodically polls the `api_call_queue` table for pending API call requests.
    - Sends POST requests to a specified API endpoint with queued data.
    - Removes successfully processed requests from the queue.
    - Waits for a specified interval between polling attempts.
    
    This function runs indefinitely in a loop.
    """
    logger.info("Starting API call watcher thread")
    
    while True:
        try:
            with SessionLocal() as db:
                # Fetch up to 10 oldest entries from the queue
                result = db.execute(
                    text("SELECT * FROM api_call_queue ORDER BY created_at ASC LIMIT 10")
                )
                
                # Convert result to list of dictionaries
                rows = result.mappings().all()
                
                ids = []  # List to collect IDs of successfully processed entries
                
                for row in rows:
                    try:
                        # Prepare and send API request
                        resp = requests.post(API_URL, json={
                            "table": row["table_name"],
                            "operation": row["operation"],
                            "changes": row["new_values"],
                            "columns": row["changed_columns"]
                        })
                        
                        # Raise exception if the request was unsuccessful
                        resp.raise_for_status()
                        
                        logger.info(f"Sent API call: {resp.status_code}")
                        ids.append(row["id"])  # Mark this entry for deletion
                        
                    except Exception as e:
                        # Log any API request failure but continue processing other rows
                        logger.error(f"API call failed: {e}")
                
                if ids:
                    # Delete successfully processed entries from the queue
                    db.execute(
                        text("DELETE FROM api_call_queue WHERE id = ANY(:ids)"),
                        {"ids": ids}
                    )
                    db.commit()
                    
        except Exception as e:
            # Log any unexpected error in the worker loop
            logger.error(f"Error in api_call_worker: {e}")
        
        # Wait before checking the queue again
        time.sleep(5)
