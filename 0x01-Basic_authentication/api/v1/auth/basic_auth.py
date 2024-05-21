#!/usr/bin/env python3
"""
BasicAuth module for managing basic HTTP authentication in a Flask application.
"""

from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 encoded string.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded string as a UTF-8 string, or None if input is
                 invalid or not a valid Base64.
        """
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64.b64decode(base64_authorization_header)
            return base64_bytes.decode('utf-8')
        except (base64.binascii.Error, ValueError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user credentials from a Base64 decoded authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded string
                                                       containing the
                                                       credentials.

        Returns:
            tuple: (email, password) if valid, otherwise (None, None) if the
                   string is invalid or doesn't contain a colon.
        """
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
