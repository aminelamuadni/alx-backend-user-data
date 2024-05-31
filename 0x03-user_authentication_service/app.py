#!/usr/bin/env python3
"""
A simple Flask application that returns a greeting message in JSON format.
"""
from flask import Flask, make_response, redirect, request, jsonify, abort
from flask import url_for
from auth import Auth

# Instantiate the Auth object
AUTH = Auth()

# Initialize the Flask application
app = Flask(__name__)


# Define a route for the application
@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint which returns a JSON message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """
    Register a user with the provided email and password.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        # Try to register the user using the Auth class
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        # If the user already exists, return an error message
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    Log in a user and set the session ID in a cookie.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if login is valid
    if AUTH.valid_login(email, password):
        # Create a new session
        session_id = AUTH.create_session(email)

        # Prepare response
        response = make_response(jsonify({"email": email,
                                          "message": "logged in"}))
        response.set_cookie('session_id', session_id)
        return response
    else:
        # If login is invalid, return 401 Unauthorized
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Log out a user by destroying their session and redirecting to the home
    page.
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403, 'No session ID provided.')

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403, 'No user found for this session.')

    # Destroy the user's session
    AUTH.destroy_session(user.id)

    # Redirect to home page after successful logout
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET'])
def profile():
    """
    Retrieve and display the user's profile information if the session is
    valid.
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403, 'Session ID is missing.')

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403, 'Invalid session ID or user does not exist.')

    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Generate a reset password token for the user with the given email.
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"message": "Email is required"}), 400

    try:
        # Attempt to generate a reset password token
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        # If no user is found with the provided email, return a 403 error
        abort(403, description="No user found with the provided email")


# Run the application if this file is executed as the main program
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
