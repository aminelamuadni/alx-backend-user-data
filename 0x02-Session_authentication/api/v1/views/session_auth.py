#!/usr/bin/env python3
"""
Handles session authentication for the API. This module defines routes for
managing session login, allowing users to establish a session via a POST
request.
"""

from flask import request, jsonify, abort, make_response
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles the POST request for user login. It validates the user's email and
    password, and if correct, sets a session ID cookie.
    """
    from api.v1.app import auth

    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = make_response(user.to_json())
    session_name = os.getenv('SESSION_NAME', 'session_id')
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    Logs out the user by deleting the session ID.

    Returns:
        json: Empty dictionary if successful, or a 404 error if unsuccessful.
    """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
