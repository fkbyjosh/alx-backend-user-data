#!/usr/bin/env python3
"""
Main Flask application module for API version 1.

This module initializes and configures the Flask application server for the API,
including authentication setup, CORS configuration, route registration, and
error handling. It supports multiple authentication types and implements
request filtering for protected endpoints.
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")

if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif AUTH_TYPE == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.before_request
def bef_req():
    """
    Filter and authenticate each incoming request before routing to handlers.
    
    This function executes before every request to the Flask application.
    It handles user authentication by setting the current user on the request
    object and validates access to protected endpoints. Requests to excluded
    paths bypass authentication, while protected endpoints require valid
    authorization headers or session cookies.
    """
    if auth is None:
        pass
    else:
        setattr(request, "current_user", auth.current_user(request))
        excluded = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
        ]
        if auth.require_auth(request.path, excluded):
            cookie = auth.session_cookie(request)
            if auth.authorization_header(request) is None and cookie is None:
                abort(401, description="Unauthorized")
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handle HTTP 404 Not Found errors and return JSON response.
    
    This error handler is triggered when a requested resource or endpoint
    cannot be found on the server. It returns a standardized JSON error
    response with appropriate HTTP status code.
    
    Args:
        error: The error object containing details about the 404 error
        
    Returns:
        str: JSON response containing error message and 404 status code
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handle HTTP 401 Unauthorized errors and return JSON response.
    
    This error handler is triggered when a client attempts to access a
    protected resource without proper authentication credentials. It returns
    a standardized JSON error response indicating authentication is required.
    
    Args:
        error: The error object containing details about the 401 error
        
    Returns:
        str: JSON response containing error message and 401 status code
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handle HTTP 403 Forbidden errors and return JSON response.
    
    This error handler is triggered when an authenticated client attempts
    to access a resource they don't have permission to view or modify.
    It returns a standardized JSON error response indicating access is denied.
    
    Args:
        error: The error object containing details about the 403 error
        
    Returns:
        str: JSON response containing error message and 403 status code
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
