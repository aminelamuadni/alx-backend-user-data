#!/usr/bin/env python3
"""
Auth module for handling authentication in the API
"""

from flask import request
from typing import List, TypeVar

User = TypeVar('User')  # Generic type for user object


class Auth:
    """
    Auth class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if the API path requires authentication.
        """
        return False  # This will be expanded later.

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the Authorization header from the Flask request object.
        """
        return None  # To be implemented.

    def current_user(self, request=None) -> User:
        """
        Method to get the current user from the request.
        """
        return None  # To be implemented later.
