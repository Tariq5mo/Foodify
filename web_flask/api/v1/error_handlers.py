#!/usr/bin/env python3
"""This module contains the error handlers for the API.
"""
from flask import jsonify, request, redirect
from web_flask.api.v1.views import app_views


@app_views.app_errorhandler(404)
def not_found(error):
    """Error handler for 404 error for API routes"""
    if request.path.startswith('/api'):
        return jsonify({"error": "Not found"}), 404
    return redirect('/')


@app_views.app_errorhandler(400)
def bad_request(error):
    """Error handler for 400 error
    """
    if request.path.startswith('/api'):
        return jsonify({"error": "Bad request"}), 400
    return "Error\n", 404


@app_views.app_errorhandler(500)
def internal_error(error):
    """Error handler for 500 error
    """
    if request.path.startswith('/api'):
        return jsonify({"error": "Internal server error"}), 500
    return 'Error\n', 404
