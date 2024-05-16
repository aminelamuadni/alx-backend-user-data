#!/usr/bin/env python3
"""
This module provides functionality to obfuscate specified fields in log
messages.
"""

import re
import logging
from typing import List


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


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class that filters specified fields in log messages.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        original_format = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_format,
                            self.SEPARATOR)