#!/usr/bin/env python3
"""
Auth class for authentication and authorization
"""

from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    """
    Auth class for authentication and authorization
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path

        Args:
            path (str): The path to check
            excluded_paths (List[str]): List of excluded paths

        Returns:
            bool: False (will be implemented later)
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from a request

        Args:
            request (flask.Request, optional): The request object. Defaults to None.

        Returns:
            str: None (will be implemented later)
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user from a request

        Args:
            request (flask.Request, optional): The request object. Defaults to None.

        Returns:
            User: None (will be implemented later)
        """
        return None
