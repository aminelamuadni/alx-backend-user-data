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
        Determine if the API path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that don't require
                                        authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None or not excluded_paths:
            return True
        path = path.strip('/')

        for excluded_path in excluded_paths:
            formatted_path = excluded_path.strip('/')
            if path == formatted_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the Authorization header from the request if available.

        Args:
            request (Request): Flask request object

        Returns:
            str: The value of the Authorization header, None if not present
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> User:
        """
        Method to get the current user from the request.
        """
        return None  # To be implemented later.
