#!/usr/bin/env python3
"""
"""
from flask import jsonify
from api import app_views
from models import storage


@app_views.route("/clients", strict_slashes=False)
def get_restaurants():
    """ """
    return jsonify(storage.all("Restaurant"))


@app_views.route("/clients/<id>", strict_slashes=False)
def get_restaurant(id):
    """Get specific client"""
    return id
