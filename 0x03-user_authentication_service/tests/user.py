#!/usr/bin/env python3
"""
This module defines the User model for the users table using SQLAlchemy.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    User model for the users table.

    Attributes:
        id (int): The primary key of the user.
        email (str): The email of the user. Non-nullable and unique.
        hashed_password (str): The hashed password of the user. Non-nullable.
        session_id (str): The session ID of the user. Nullable.
        reset_token (str): The reset token for password reset. Nullable.
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    session_id = db.Column(db.String(255), nullable=True)
    reset_token = db.Column(db.String(255), nullable=True)
