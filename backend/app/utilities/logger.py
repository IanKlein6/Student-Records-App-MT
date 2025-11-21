# app/utilities/logger.py

"""Logger Configs.

Configuration and centralizing of loggers to help keep logging simple, readable and in one place. 

Loggers: 
    create_logger:
    query_logger:
    delete_logger:
    error_logger:

Info:
    - Change logger basicConfig setting once in production.
    - Add extra loggers as needed.
"""

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Create logs/folder if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Rotating file handler
file_handler = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=3)


# Configure root logger 
logging.basicConfig(
    level=logging.DEBUG, ### set to INFO or WARNING in production
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        file_handler,
        logging.StreamHandler()
    ]
)


# Action-based named loggers. Add more as needed here -
create_logger = logging.getLogger("CREATE")
query_logger = logging.getLogger("QUERY")
delete_logger = logging.getLogger("DELETE")
error_logger = logging.getLogger("ERROR")