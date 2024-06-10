#!/usr/bin/env python3
"""
This module defines the User model for the users table using SQLAlchemy.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """
    User model for the users table.

    Attributes:
        id (int): The primary key of the user.
        email (str): The email of the user. Non-nullable and unique.
        hashed_password (str): The hashed password of the user. Non-nullable.
        session_id (str): The session ID of the user. Nullable.
        reset_token (str): The reset token for password reset. Nullable.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    session_id = Column(String(255), nullable=True)
    reset_token = Column(String(255), nullable=True)
