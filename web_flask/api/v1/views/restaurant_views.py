#!/usr/bin/env python3
"""This module contains the view for the restaurant
"""
from flask import jsonify
from api import app_views
from models import storage


@app_views.route('/restaurants', strict_slashes=False)
def get_restaurants():
    """This function retrieves all restaurants
    """
    return jsonify(storage.all("Restaurant"))


@app_views.route('/restaurants/<id>', strict_slashes=False)
def get_restaurant(id):
    """Get specific restaurant"""
    return id
