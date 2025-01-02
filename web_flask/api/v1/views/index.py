#!/usr/bin/python3
"""This module contains the index views for the API.
"""
from web_flask.api.v1.views import app_views
from flask import jsonify
from models.clients import Client
from models.restaurant import Restaurant
from models.menu_item import MenuItem
from models.review import Review
from models.orders import Order
from models.order_items import OrderItem
from models import storage


classes = {
    "Client": Client,
    "Restaurant": Restaurant,
    "MenuItem": MenuItem,
    "Review": Review,
    "Order": Order,
    "OrderItem": OrderItem,
}


@app_views.route("/stats")
def num_objs():
    """Retrieves the number of each objects by type"""
    di = {}
    for cls in classes:
        di[classes[cls]] = storage.count(cls)
    return jsonify(di)


@app_views.route("/status", strict_slashes=False)
def foo_status():
    """Return the status"""
    return jsonify({"status": "OK"})
