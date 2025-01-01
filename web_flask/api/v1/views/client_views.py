#!/usr/bin/env python3
"""This module contains the client views for the API.
"""
from email.policy import strict
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


@app_views.route("/clients", methods=["POST"], strict_slashes=False)
def post_Client():
    """Create a new client"""
    return "POST"


@app_views.route("/clients/<id>", methods=["PUT"], strict_slashes=False)
def put_Client(id):
    """Update a client"""
    return id


@app_views.route("/clients/<id>", methods=["DELETE"], strict_slashes=False)
def delete_Client(id):
    """Delete a client"""
    return id


@app_views.route("/clients/<id>/orders", strict_slashes=False)
def get_Client_orders(id):
    """Get all orders for a specific client"""
    return id


@app_views.route("/clients/<id>/orders", methods=["POST"], strict_slashes=False)
def post_Client_orders(id):
    """Create a new order for a specific client"""
    return id


@app_views.route("/clients/<id>/orders/<order_id>", strict_slashes=False)
def get_Client_order(id, order_id):
    """Get a specific order for a specific client"""
    return id


@app_views.route("/clients/<id>/orders/<order_id>", methods=["PUT"], strict_slashes=False)
def put_Client_order(id, order_id):
    """Update a specific order for a specific client"""
    return id


@app_views.route("/clients/<id>/orders/<order_id>", methods=["DELETE"], strict_slashes=False)
def delete_Client_order(id, order_id):
    """Delete a specific order for a specific client"""
    return id


@app_views.route("/clients/<id>/orders/<order_id>/items", strict_slashes=False)
def get_Client_order_items(id, order_id):
    """Get all items for a specific order for a specific client"""
    return id


@app_views.route("/clients/<id>/orders/<order_id>/items", methods=["POST"], strict_slashes=False)
def post_Client_order_items(id, order_id):
    """Create a new item for a specific order for a specific client"""
    return id


@app_views.route("/clients/<id>/orders/<order_id>/items/<item_id>", strict_slashes=False)
def get_Client_order_item(id, order_id, item_id):
    """Get a specific item for a specific order for a specific client"""
    return id


@app_views.route("/clients/<id>/orders/<order_id>/items/<item_id>", methods=["PUT"], strict_slashes=False)
def put_Client_order_item(id, order_id, item_id):
    """Update a specific item for a specific order for a specific client"""
    return id


@app_views.route("/clients/<id>/orders/<order_id>/items/<item_id>", methods=["DELETE"], strict_slashes=False)
def delete_Client_order_item(id, order_id, item_id):
    """Delete a specific item for a specific order for a specific client"""
    return id
