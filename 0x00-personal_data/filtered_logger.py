#!/usr/bin/env python3
"""
This module provides functionality to obfuscate specified fields in log
messages.
"""

import re
import logging
import os
import mysql.connector
from datetime import datetime
from typing import List

# Define PII fields
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Arguments:
    fields -- list of fields to obfuscate
    redaction -- replacement value for the fields
    message -- log message to process
    separator -- character that separates fields in the log message

    Returns:
    A log message with specified fields obfuscated.
    """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """
    Configures and returns a logger with specified settings to handle user
    data.

    Returns:
        logging.Logger: Configured logger with redaction formatting.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a stream handler with specific formatting
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the MySQL database using environment variables and returns
    the connection object.

    Returns:
        MySQLConnection: A connection to the database.
    """
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME', '')

    return mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        port=3306,
        database=db_name
    )


def main():
    """ Log user data from a database, obfuscating sensitive fields. """
    logger = get_logger()
    connection = get_db()
    cursor = connection.cursor()
    query = """
        SELECT name, email, phone, ssn, password, ip, last_login, user_agent
        FROM users
    """
    cursor.execute(query)
    results = cursor.fetchall()

    for result in results:
        ip = result[5]
        last_login_str = datetime.strftime(result[6], "%Y-%m-%dT%H:%M:%S")
        user_agent = result[7]
        log_message = (
            f"name=***; email=***; phone=***; ssn=***; password=***; "
            f"ip={ip}; last_login={last_login_str}; user_agent={user_agent};"
        )
        logger.info(log_message)

    cursor.close()
    connection.close()


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class that filters specified fields in log messages.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter.

        Args:
            fields (List[str]): List of fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record and applies data filtering.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log record with filtered data.
        """
        original_format = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_format,
                            self.SEPARATOR)


if __name__ == "__main__":
    main()
