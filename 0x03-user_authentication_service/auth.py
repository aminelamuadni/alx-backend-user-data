#!/usr/bin/env python3
"""
Authentication module for handling password security.
"""

import uuid
import bcrypt
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt, incorporating a salt for added security.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted and hashed password as a byte string.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate a new UUID and return it as a string.

    Returns:
        str: A new UUID as a string.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user in the database.

        Args:
            email (str): The email of the user to register.
            password (str): The user's password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login attempt.

        Args:
            email (str): The email of the user trying to log in.
            password (str): The password provided by the user for login.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
                return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        Create a session ID for a user based on email.

        Args:
            email (str): The email of the user.

        Returns:
            str: A new session ID as a string if the user exists, otherwise
                 None.
        """
        user = self._db.find_user_by(email=email)
        if not user:
            return None

        # Generate a new UUID for the session ID
        session_id = str(uuid.uuid4())

        # Store the session ID in the database
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str):
        """
        Retrieve a user from the database using the session ID.

        Args:
            session_id (str): The session ID of the user to retrieve.

        Returns:
            User or None: The user object if found, otherwise None.
        """
        if session_id is None:
            return None

        try:
            # Find the user by session_id
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Invalidate a user session by setting their session ID to None.

        Args:
            user_id (int): The ID of the user whose session is to be destroyed.

        Returns:
            None
        """
        # Update the user's session ID to None
        self._db.update_user(user_id, session_id=None)
