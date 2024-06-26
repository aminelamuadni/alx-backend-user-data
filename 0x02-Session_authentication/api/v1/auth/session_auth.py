#!/usr/bin/env python3
"""
Session authentication management for a Flask application.
"""

import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth class for handling session-based authentication by storing user
    sessions.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a specific user ID.

        Args:
            user_id (str): The user ID for which to create a session.

        Returns:
            str: A new session ID, or None if the user_id is None or not a
                 string.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves a user ID based on a session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID associated with the session ID, or None if not
                 found or invalid input.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves a User instance based on a cookie value from the request.

        Args:
            request (Request): Flask request object.

        Returns:
            User: The user instance associated with the session ID, or None if
                  not found.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id:
            return User.get(user_id)
        return None

    def destroy_session(self, request=None):
        """
        Deletes the user session / logs out the user.

        Args:
            request (Request): Flask request object.

        Returns:
            bool: True if the session was successfully destroyed, otherwise
                  False.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None or not self.user_id_for_session_id(session_id):
            return False

        self.user_id_by_session_id.pop(session_id, None)
        return True
