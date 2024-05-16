#!/usr/bin/env python3
"""
This module provides functionality to hash passwords securely.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with bcrypt.

    Args:
    password (str): The plaintext password to hash.

    Returns:
    bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password.

    Args:
    hashed_password (bytes): The hashed password.
    password (str): The plaintext password to validate.

    Returns:
    bool: True if the password is correct, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
