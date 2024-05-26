#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Authentication setup
auth_type = getenv("AUTH_TYPE")
if auth_type == 'session_db_auth':
    auth = SessionDBAuth()
elif auth_type == 'session_exp_auth':
    auth = SessionExpAuth()
elif auth_type == 'session_auth':
    auth = SessionAuth()
elif auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'auth':
    auth = Auth()
else:
    auth = None


@app.before_request
def before_request_func():
    """
    Function to run before each request to validate authentication and
    permissions.
    Also, assigns the current user from the request to the global request
    context.
    """
    # Paths that don't require authentication
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']
    if auth is None or not auth.require_auth(request.path, excluded_paths):
        return  # Skip authentication for excluded paths

    if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
        abort(401)  # No auth header or session cookie

    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)  # No user found


@app.errorhandler(401)
def unauthorized(error):
    """Error handler for 401 Unauthorized errors."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """Error handler for 403 Forbidden errors."""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
