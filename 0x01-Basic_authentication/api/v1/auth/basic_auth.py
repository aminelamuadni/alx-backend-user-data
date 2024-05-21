#!/usr/bin/env python3
"""
BasicAuth module for managing basic HTTP authentication in a Flask application.
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class for handling basic HTTP authentication.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 encoded part of the Authorization header.

        Args:
            authorization_header (str): The content of the Authorization header
                                        from the request.

        Returns:
            str: The Base64 encoded part of the header, or None if the header
                 is invalid or not present.
        """
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        # Extract the part after "Basic "
        return authorization_header[6:]
