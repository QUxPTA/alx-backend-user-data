#!/usr/bin/env python3
"""
Session authentication module.
"""

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    SessionAuth class for session-based authentication.
    Currently, this class does not add any new functionality
    to the inherited Auth class.
    """
    pass
