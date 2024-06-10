#!/usr/bin/env python3
"""auth module
"""
import bcrypt
from db import DB, User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the provided email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        try:
            # Check if the user already exists
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User does not exist, proceed to create one
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                email=email, hashed_password=hashed_password)
            return new_user
