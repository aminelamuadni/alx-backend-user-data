#!/usr/bin/env python3
"""
SessionDBAuth module for managing sessions using database storage.
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Handles session management with sessions stored in a database.
    """

    def create_session(self, user_id=None):
        """
        Creates a session stored in the database.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        new_session = UserSession(user_id=user_id, session_id=session_id)
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with a given session ID.
        """
        if session_id is None:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None
        session_data = user_session[0]
        if self.session_duration > 0:
            start_time = datetime.fromisoformat(session_data.created_at)
            if datetime.now() > (start_time + timedelta(
                seconds=self.session_duration)):
                session_data.remove()
                return None
        return session_data.user_id

    def destroy_session(self, request=None):
        """
        Destroys a session based on the Session ID from the request cookie.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
