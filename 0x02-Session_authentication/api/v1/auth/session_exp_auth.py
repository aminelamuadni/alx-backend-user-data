#!/usr/bin/env python3
"""
SessionExpAuth module for handling session-based authentication with
expiration.
"""

import uuid
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class for managing session-based authentication with an
    expiration time.
    """

    def __init__(self):
        """
        Initialize the session expiration duration based on environment
        variable SESSION_DURATION.
        """
        session_duration = os.getenv('SESSION_DURATION', 0)
        try:
            self.session_duration = int(session_duration)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session with an expiration time.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID from the session dictionary if the session has
        not expired.
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']

        if 'created_at' not in session_dict:
            return None

        session_start = session_dict['created_at']
        session_end = session_start + timedelta(seconds=self.session_duration)
        if session_end < datetime.now():
            return None

        return session_dict['user_id']
