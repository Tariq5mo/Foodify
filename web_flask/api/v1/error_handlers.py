#!/usr/bin/env python3
"""This module contains the error handlers for the API.
"""
from api import app_views


@app_views.errorhandler(404)
def not_found(error):
    """Error handler for 404 error
    """
    return {"error": "Not found"}, 404


@app_views.errorhandler(400)
def bad_request(error):
    """Error handler for 400 error
    """
    return {"error": "Bad request"}, 400


@app_views.errorhandler(500)
def internal_error(error):
    """Error handler for 500 error
    """
    return {"error": "Internal server error"}, 500
