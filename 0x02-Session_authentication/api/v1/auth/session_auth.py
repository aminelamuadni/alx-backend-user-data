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
