#!/usr/bin/env python3
"""
This module provides functionality to obfuscate specified fields in log
messages.
"""

import re


def filter_datum(fields, redaction, message, separator):
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
