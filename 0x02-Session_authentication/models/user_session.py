#!/usr/bin/env python3
"""
UserSession module for managing session data in the database.
"""
from models.base import Base


class UserSession(Base):
    """
    UserSession class for storing session IDs linked to user IDs.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a new instance of the UserSession class.

        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.

        Attributes:
            user_id (str): The ID of the user associated with the session.
            session_id (str): The ID of the session.

        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
