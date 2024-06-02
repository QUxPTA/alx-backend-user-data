#!/usr/bin/env python3
"""
Personal Data logging tasks
"""
import logging
import re
from typing import List

PII_FIELDS = ("name", "email", "phone", "SSN", "password")


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (list): List of strings representing all fields to obfuscate.
        redaction (str): String representing by what the field will be obfuscated.
        message (str): String representing the log line.
        separator (str): String representing by which character is separating all fields in the log line.

    Returns:
        str: The obfuscated log message.
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with specified fields to obfuscate.

        Args:
            fields (list): List of strings representing all fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by obfuscating specified fields.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log record with obfuscated fields.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


if __name__ == '__main__':
    main()
