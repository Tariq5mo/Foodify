#!/usr/bin/env python3
"""This module contains the client views for the API.
"""
from flask import jsonify, request, abort
from models import storage
from models.clients import Client
from models.orders import Order
from models.review import Review
from api.v1.views import app_views


@app_views.route("/clients", methods=["GET"], strict_slashes=False)
def get_clients():
    """Retrieve all clients"""
    clients = storage.all(Client)
    return jsonify([client.to_dict() for client in clients.values()])


@app_views.route("/clients/<id>", methods=["GET"], strict_slashes=False)
def get_client(id):
    """Retrieve a client by ID"""
    client = storage.get(Client, id)
    if not client:
        abort(404)
    return jsonify(client.to_dict())


@app_views.route("/clients", methods=["POST"], strict_slashes=False)
def create_client():
    """Create a new client"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data or "email" not in data:
        abort(400, "Missing name or email")
    client = Client(**data)
    client.save()
    return jsonify(client.to_dict()), 201


@app_views.route("/clients/<id>", methods=["PUT"], strict_slashes=False)
def update_client(id):
    """Update a client"""
    client = storage.get(Client, id)
    if not client:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(client, key, value)
    client.save()
    return jsonify(client.to_dict())


@app_views.route("/clients/<id>", methods=["DELETE"], strict_slashes=False)
def delete_client(id):
    """Delete a client"""
    client = storage.get(Client, id)
    if not client:
        abort(404)
    client.delete()
    return jsonify({}), 200


# Client Orders
@app_views.route(
    "/clients/<id>/orders", methods=["GET"], strict_slashes=False
)
def get_client_orders(id):
    """Get all orders for a client"""
    client = storage.get(Client, id)
    if not client:
        abort(404)
    return jsonify([order.to_dict() for order in client.orders])


@app_views.route(
    "/clients/<id>/orders", methods=["POST"], strict_slashes=False
)
def create_client_order(id):
    """Create a new order for a client"""
    client = storage.get(Client, id)
    if not client:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "restaurant_id" not in data or "menu_items" not in data:
        abort(400, "Missing restaurant_id or menu_items")
    data["client_id"] = id
    order = Order(**data)
    order.save()
    return jsonify(order.to_dict()), 201


# Client Reviews
@app_views.route(
    "/clients/<id>/reviews", methods=["GET"], strict_slashes=False
)
def get_client_reviews(id):
    """Get all reviews by a client"""
    client = storage.get(Client, id)
    if not client:
        abort(404)
    return jsonify([review.to_dict() for review in client.reviews])


@app_views.route(
    "/clients/<id>/reviews", methods=["POST"], strict_slashes=False
)
def create_client_review(id):
    """Create a new review by a client"""
    client = storage.get(Client, id)
    if not client:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "restaurant_id" not in data or "rating" not in data:
        abort(400, "Missing restaurant_id or rating")
    data["client_id"] = id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201
