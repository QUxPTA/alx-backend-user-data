#!/usr/bin/env python3
"""
Session authentication module.
"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    SessionAuth class for session-based authentication.
    This class provides methods to create and manage session IDs.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a Session ID for a given user_id.

        Args:
            user_id (str): The user ID for which to create a session.

        Returns:
            str: The Session ID if user_id is valid, otherwise None.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Return a User ID based on a Session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The User ID if session_id is valid, otherwise None.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
