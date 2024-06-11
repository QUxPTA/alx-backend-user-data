#!/usr/bin/env python3
"""Basic Flask app module for user registration and login."""
from flask import Flask, redirect, request, jsonify, abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """
    GET /
    Return a JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    POST /users
    Register a new user.

    Expects form data fields: "email" and "password".
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    POST /sessions
    Log in a user.

    Expects form data fields: "email" and "password".
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Handle user logout.

    Sends a DELETE request to /sessions. If the request is successful,
    it returns a message.

    Returns:
        str: A message indicating the success of the logout operation.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Retrieve the user's profile information.

    Sends a GET request to /profile. If the request is successful, it returns
    the user's email as a JSON payload.

    Returns:
        str: A JSON payload containing the user's email.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """Handle the request to generate a reset password token.

    POST /reset_password

    Expects form data field: "email".

    Returns:
        str: A JSON object containing the email and the generated reset token.

    Raises:
        HTTPException: If the user does not exist,
        returns a 403 HTTP status code.
    """
    email = request.form.get('email')
    user = AUTH.create_session(email)
    if not user:
        abort(403)
    else:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Handle the request to update a user's password.

    PUT /reset_password

    Expects form data fields: "email", "reset_token", and "new_password".

    Returns:
        str: A JSON object containing the email and a success message.

    Raises:
        HTTPException: If an error occurs during password update,
        returns a 403 HTTP status code.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_psw = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_psw)
        return jsonify({"email": f"{email}",
                        "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
