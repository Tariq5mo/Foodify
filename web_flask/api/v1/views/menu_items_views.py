#!/usr/bin/env python3
"""
"""
from flask import jsonify
from api import app_views
from models import storage


@app_views.route("/menu_items", strict_slashes=False)
def get_restaurants():
    """ """
    return jsonify(storage.all("Restaurant"))


@app_views.route("/menu_items/<id>", strict_slashes=False)
def get_restaurant(id):
    """Get specific restaurant"""
    return id
