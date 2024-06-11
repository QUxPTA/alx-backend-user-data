#!/usr/bin/env python3
"""
Auth module
"""
import uuid
import bcrypt
from db import DB, User
from sqlalchemy.exc import NoResultFound, InvalidRequestError


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


def _generate_uuid() -> str:
    """
    Generate a new UUID.

    Returns:
        str: The string representation of the UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initialize a new Auth instance.

        This constructor initializes a new instance of the Auth class and 
        creates an instance of the DB class for database interactions.
        """
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
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User does not exist, proceed to create one
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                email=email, hashed_password=hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            # Locate the user by email
            user = self._db.find_user_by(email=email)
            # Check if the provided password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Create a session for a user and return the session ID.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID, or None if no user is found.
        """
        try:
            # Locate the user by email
            user = self._db.find_user_by(email=email)
            # Generate a new UUID for the session ID
            session_id = _generate_uuid()
            # Update the user's session_id in the database
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
        except InvalidRequestError:
            raise ValueError("Invalid query arguments")
