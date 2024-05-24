#!/usr/bin/env python3
"""
SessionDBAuth module for managing sessions using database storage.
"""
from datetime import datetime, timedelta
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    Handles session management with sessions stored in a database.
    """

    def create_session(self, user_id=None) -> str:
        """
        Create a session ID for a user_id and save it to the database.

        Args:
            user_id (str): The ID of the user for whom the session is being
                           created.

        Returns:
            str: The session ID generated for the user.

        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kwargs = {
            "user_id": user_id,
            "session_id": session_id
        }
        new_session = UserSession(**kwargs)
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve a user ID from a session ID with consideration for session
        expiration.

        Args:
            session_id (str): The session ID to retrieve the user ID for.

        Returns:
            int or None: The user ID associated with the session ID, or None if
            the session ID is invalid or expired.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        try:
            user_sessions = UserSession.search({'session_id': session_id})
            if not user_sessions:
                return None

            user_session = user_sessions[0]
            # Calculate the expiration time
            session_start = user_session.created_at
            session_end = session_start + timedelta(
                seconds=self.session_duration)
            if session_end < datetime.now():
                # Session has expired
                return None

            return user_session.user_id
        except Exception as e:
            return None

    def destroy_session(self, request=None) -> bool:
        """
        Destroy a session based on the session ID from the request cookie.

        Args:
            request (Request): The request object containing the session ID.

        Returns:
            bool: True if the session was successfully destroyed, False
                  otherwise.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
