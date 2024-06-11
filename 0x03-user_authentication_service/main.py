#!/usr/bin/env python3
"""Main module for testing user authentication and management."""

import requests

BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user."""
    response = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200, "Failed to register user"
    assert response.json() == {
        "email": email, "message": "user created"}, "Unexpected response payload"


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with a wrong password."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 401, "Expected login to fail with wrong password"


def log_in(email: str, password: str) -> str:
    """Log in with correct credentials and return the session ID."""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={"email": email, "password": password})
    assert response.status_code == 200, "Failed to log in"
    session_id = response.cookies.get("session_id")
    assert session_id is not None, "No session_id cookie in response"
    return session_id


def profile_unlogged() -> None:
    """Attempt to access profile without being logged in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, "Expected access to profile to be forbidden"


def profile_logged(session_id: str) -> None:
    """Access profile while logged in."""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, "Failed to access profile"
    assert "email" in response.json(), "Email not in response payload"


def log_out(session_id: str) -> None:
    """Log out a user."""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, "Failed to log out"


def reset_password_token(email: str) -> str:
    """Get a password reset token."""
    response = requests.post(
        f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, "Failed to get reset password token"
    token = response.json().get("reset_token")
    assert token is not None, "No reset token in response"
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the user's password using the reset token."""
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email, "reset_token": reset_token,
              "new_password": new_password}
    )
    assert response.status_code == 200, "Failed to update password"
    assert response.json() == {
        "email": email, "message": "Password updated"}, "Unexpected response payload"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
