"""
Configures the logging system for NoteManager API.
Logs are rotated daily and saved to a configured directory.
"""

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from datetime import datetime
import os
import configparser

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Get log directory from config, or fallback to 'logs'
log_dir = config.get("LOGGING", "LOG_DIR", fallback="logs")

# Ensure the log directory exists
Path(log_dir).mkdir(parents=True, exist_ok=True)

# Define log file path with current date
log_file = os.path.join(log_dir, f"api-{datetime.now().strftime('%d-%m-%y')}.log")

# Create logger
logger = logging.getLogger("note_manager_logger")
logger.setLevel(logging.INFO)

# Create a timed rotating file handler (daily logs)
handler = TimedRotatingFileHandler(
    filename=log_file,
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8"
)
handler.suffix = "%d-%m-%y"

# Set log format
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Attach handler to logger
logger.addHandler(handler)
logger.propagate = False
