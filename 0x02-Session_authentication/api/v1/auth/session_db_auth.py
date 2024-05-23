#!/usr/bin/env python3
"""
SessionDBAuth module for managing sessions using database storage.
"""
import uuid
from datetime import datetime
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    Handles session management with sessions stored in a database.
    """

    def create_session(self, user_id=None):
        """Create a session ID for a user_id and save it to the database."""
        session_id = str(uuid.uuid4())
        new_session = UserSession(user_id=user_id, session_id=session_id)
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve a user ID from a session ID."""
        if session_id is None:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            return user_session[0].user_id
        return None

    def destroy_session(self, request=None):
        """
        Destroy a session based on the session ID from the request cookie.
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
