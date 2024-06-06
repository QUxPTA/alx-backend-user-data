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
                bool: True if authentication is required, False otherwise
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path.rstrip('/')  # remove trailing slash
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                excluded_path = excluded_path.rstrip('*')  # remove trailing *
                if path.startswith(excluded_path):
                    return False
            else:
                excluded_path = excluded_path.rstrip(
                    '/')  # remove trailing slash
                if path == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from a request

        Args:
            request (flask.Request, optional):
            The request object. Defaults to None.

        Returns:
            str: The value of the Authorization header,
            or None if not present
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user from a request

        Args:
            request (flask.Request, optional):
            The request object. Defaults to None.

        Returns:
            User: None (will be implemented later)
        """
        return None
