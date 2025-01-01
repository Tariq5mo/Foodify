#!/usr/bin/env python3
"""This module contains the view for the menu items
"""
from flask import jsonify
from api import app_views
from models import storage


@app_views.route("/menu_items", strict_slashes=False)
def get_menu_items():
    """ This function retrieves all menu items """
    return jsonify(storage.all("MenuItem"))


@app_views.route("/menu_items/<id>", strict_slashes=False)
def get_menu_item(id):
    """Get a specific menu_items"""
    return id
