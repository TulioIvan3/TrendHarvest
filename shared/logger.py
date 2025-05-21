import logging
from logging.handlers import RotatingFileHandler
import os
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "platform": getattr(record, 'platform', 'system')
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # File Handler
    os.makedirs('logs', exist_ok=True)
    file_handler = RotatingFileHandler(
        f'logs/{name}.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(JSONFormatter())

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('%(levelname)s - %(name)s: %(message)s')
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger