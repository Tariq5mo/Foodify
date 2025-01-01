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


@app_views.route('/restaurants', methods=['POST'], strict_slashes=False)
def post_restaurant():
    """Create a new restaurant"""
    return "POST"


@app_views.route('/restaurants/<id>', methods=['PUT'], strict_slashes=False)
def put_restaurant(id):
    """Update a restaurant"""
    return id


@app_views.route('/restaurants/<id>', methods=['DELETE'], strict_slashes=False)
def delete_restaurant(id):
    """Delete a restaurant"""
    return id


@app_views.route('/restaurants/<id>/menu_items', strict_slashes=False)
def get_restaurant_menu_items(id):
    """Get all menu items for a specific restaurant"""
    return id


@app_views.route('/restaurants/<id>/menu_items', methods=['POST'], strict_slashes=False)
def post_restaurant_menu_items(id):
    """Create a new menu item for a specific restaurant"""
    return id


@app_views.route('/restaurants/<id>/menu_items/<menu_item_id>', strict_slashes=False)
def get_restaurant_menu_item(id, menu_item_id):
    """Get a specific menu item for a specific restaurant"""
    return id


@app_views.route('/restaurants/<id>/menu_items/<menu_item_id>', methods=['PUT'], strict_slashes=False)
def put_restaurant_menu_item(id, menu_item_id):
    """Update a specific menu item for a specific restaurant"""
    return id


@app_views.route('/restaurants/<id>/menu_items/<menu_item_id>', methods=['DELETE'], strict_slashes=False)
def delete_restaurant_menu_item(id, menu_item_id):
    """Delete a specific menu item for a specific restaurant"""
    return id



