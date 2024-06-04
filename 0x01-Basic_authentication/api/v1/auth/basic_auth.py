#!/usr/bin/env python3
"""
BasicAuth class for basic authentication
"""

from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class for basic authentication
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extract the Base64 part of the Authorization
        header for Basic Authentication

        Args:
            authorization_header (str): The Authorization header

        Returns:
            str: The Base64 part of the Authorization header,
            or None if invalid
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                     str) -> (str, str):
        """
        Extract the user email and password from the decoded Base64 value

        Args:
            decoded_base64_authorization_header (str): The decoded Base64 value

        Returns:
            tuple: The user email and password, or None, None if invalid
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_email, user_password = decoded_base64_authorization_header.split(
            ":", 1)
        return user_email, user_password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> User:
        """
        Return the User instance based on his email and password

        Args:
            user_email (str): The user email
            user_pwd (str): The user password

        Returns:
            User: The User instance, or None if invalid
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user
