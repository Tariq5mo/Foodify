#!/usr/bin/env python3
"""This module contains the error handlers for the API.
"""
from flask import jsonify, request
from web_flask.api.v1.views import app_views
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_error_response(error, status_code):
    """Create structured error response"""
    response = {
        "error": {
            "code": status_code,
            "message": str(error),
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.path,
            "method": request.method
        }
    }
    logger.error(f"Error {status_code}: {str(error)} - Path: {request.path}")
    return jsonify(response), status_code


@app_views.errorhandler(400)
def bad_request(error):
    """Bad Request handler"""
    return create_error_response("Bad Request", 400)


@app_views.errorhandler(404)
def not_found(error):
    """Not Found handler"""
    return create_error_response("Resource Not Found", 404)


@app_views.errorhandler(405)
def method_not_allowed(error):
    """Method Not Allowed handler"""
    return create_error_response("Method Not Allowed", 405)


@app_views.errorhandler(500)
def internal_error(error):
    """Internal Server Error handler"""
    return create_error_response("Internal Server Error", 500)
