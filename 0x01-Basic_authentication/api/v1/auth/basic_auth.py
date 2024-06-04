#!/usr/bin/env python3
"""
BasicAuth class for basic authentication
"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    BasicAuth class for basic authentication
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extract the Base64 part of the Authorization header for Basic Authentication

        Args:
            authorization_header (str): The Authorization header

        Returns:
            str: The Base64 part of the Authorization header, or None if invalid
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decode a Base64 string into a UTF-8 string

        Args:
            base64_authorization_header (str): The Base64 string to decode

        Returns:
            str: The decoded UTF-8 string, or None if invalid
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except ValueError:
            return None
