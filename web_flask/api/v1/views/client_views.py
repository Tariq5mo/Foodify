#!/usr/bin/env python3
"""This module contains the client views for the API.
"""
from flask import jsonify
from web_flask.api import app_views
from models import storage


@app_views.route("/clients", strict_slashes=False)
def get_Clients():
    """ This function retrieves all clients """
    return jsonify(storage.all("Client"))


@app_views.route("/clients/<id>", strict_slashes=False)
def get_Client(id):
    """Get a specific client"""
    return id
