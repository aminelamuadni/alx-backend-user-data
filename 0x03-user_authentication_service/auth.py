"""
Authentication module for handling password security.
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt, incorporating a salt for added security.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted and hashed password as a byte string.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
