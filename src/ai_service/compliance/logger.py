# src/ai_service/compliance/logger.py
# Copyright (c) 2023 Your Company. All rights reserved.

import logging
from datetime import datetime
import os

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with the given name.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

class AuditLogger:
    def __init__(self, log_dir: str):
        """
        Initialize the AuditLogger with the given log directory.

        Args:
            log_dir (str): The directory to store logs.
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

    def log_generation(self, user: str, prompt: str) -> None:
        """
        Log the generation event to a file.

        Args:
            user (str): The user who initiated the generation.
            prompt (str): The prompt used for generation.
        """
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        log_message = f"User: {user}, Prompt: {prompt}, Timestamp: {timestamp}"
        self.write_to_file(log_message, f"{self.log_dir}/{user}_{timestamp}.log")

    def write_to_file(self, message: str, filepath: str) -> None:
        """
        Write a log message to a file.

        Args:
            message (str): The log message to write.
            filepath (str): The file path for the log file.
        """
        try:
            with open(filepath, 'a') as log_file:
                log_file.write(message + '\n')
            logging.info(f"Successfully wrote log to file: {filepath}")
        except Exception as e:
            logging.error(f"Failed to write log to file: {e}")

# Example usage
if __name__ == "__main__":
    logger = setup_logger("audit_logger")
    audit_logger = AuditLogger("/tmp/logs")
    audit_logger.log_generation("test_user", "test_prompt")
