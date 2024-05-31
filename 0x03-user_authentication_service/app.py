#!/usr/bin/env python3
"""
A simple Flask application that returns a greeting message in JSON format.
"""
from flask import Flask, make_response, request, jsonify, abort
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


# Run the application if this file is executed as the main program
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
