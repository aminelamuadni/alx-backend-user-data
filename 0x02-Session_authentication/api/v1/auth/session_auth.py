#!/usr/bin/env python3
"""
Session authentication management for a Flask application.
"""

import uuid
from api.v1.auth.auth import Auth


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
