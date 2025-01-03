#!/usr/bin/env python3
"""This module contains the view for the restaurant
"""
from flask import jsonify, request, abort
from web_flask.api.v1.views import app_views
from models import storage
from models.restaurant import Restaurant
from models.menu_item import MenuItem
from models.review import Review


# Restaurant CRUD
@app_views.route("/restaurants", methods=["GET"], strict_slashes=False)
def get_restaurants():
    """Retrieve all restaurants"""
    restaurants = storage.all(Restaurant)
    return jsonify(
        [restaurant.to_dict() for restaurant in restaurants.values()]
    )


@app_views.route("/restaurants/<id>", methods=["GET"], strict_slashes=False)
def get_restaurant(id):
    """Retrieve a restaurant by ID"""
    restaurant = storage.get(Restaurant, id)
    if not restaurant:
        abort(404)
    return jsonify(restaurant.to_dict())


@app_views.route("/restaurants", methods=["POST"], strict_slashes=False)
def create_restaurant():
    """Create a new restaurant"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data or "location" not in data:
        abort(400, "Missing name or location")
    restaurant = Restaurant(**data)
    restaurant.save()
    return jsonify(restaurant.to_dict()), 201


@app_views.route("/restaurants/<id>", methods=["PUT"], strict_slashes=False)
def update_restaurant(id):
    """Update a restaurant"""
    restaurant = storage.get(Restaurant, id)
    if not restaurant:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(restaurant, key, value)
    restaurant.save()
    return jsonify(restaurant.to_dict())


@app_views.route(
    "/restaurants/<id>", methods=["DELETE"], strict_slashes=False
)
def delete_restaurant(id):
    """Delete a restaurant"""
    restaurant = storage.get(Restaurant, id)
    if not restaurant:
        abort(404)
    restaurant.delete()
    return jsonify({}), 200


# MenuItem CRUD within Restaurant
@app_views.route(
    "/restaurants/<id>/menu_items", methods=["GET"], strict_slashes=False
)
def get_restaurant_menu_items(id):
    """Get all menu items for a specific restaurant"""
    restaurant = storage.get(Restaurant, id)
    if not restaurant:
        abort(404)
    return jsonify([item.to_dict() for item in restaurant.menu_items])


@app_views.route(
    "/restaurants/<id>/menu_items", methods=["POST"], strict_slashes=False
)
def create_restaurant_menu_item(id):
    """Create a new menu item for a specific restaurant"""
    restaurant = storage.get(Restaurant, id)
    if not restaurant:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data or "price" not in data:
        abort(400, "Missing name or price")
    data["restaurant_id"] = id
    menu_item = MenuItem(**data)
    menu_item.save()
    return jsonify(menu_item.to_dict()), 201


@app_views.route(
    "/restaurants/<id>/menu_items/<menu_item_id>",
    methods=["GET"],
    strict_slashes=False,
)
def get_restaurant_menu_item(id, menu_item_id):
    """Get a specific menu item for a specific restaurant"""
    menu_item = storage.get(MenuItem, menu_item_id)
    if not menu_item or menu_item.restaurant_id != id:
        abort(404)
    return jsonify(menu_item.to_dict())


@app_views.route(
    "/restaurants/<id>/menu_items/<menu_item_id>",
    methods=["PUT"],
    strict_slashes=False,
)
def update_restaurant_menu_item(id, menu_item_id):
    """Update a menu item for a specific restaurant"""
    menu_item = storage.get(MenuItem, menu_item_id)
    if not menu_item or menu_item.restaurant_id != id:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "restaurant_id"]:
            setattr(menu_item, key, value)
    menu_item.save()
    return jsonify(menu_item.to_dict())


@app_views.route(
    "/restaurants/<id>/menu_items/<menu_item_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_restaurant_menu_item(id, menu_item_id):
    """Delete a menu item for a specific restaurant"""
    menu_item = storage.get(MenuItem, menu_item_id)
    if not menu_item or menu_item.restaurant_id != id:
        abort(404)
    menu_item.delete()
    return jsonify({}), 200


# Review CRUD for Restaurants
@app_views.route(
    "/restaurants/<id>/reviews", methods=["GET"], strict_slashes=False
)
def get_restaurant_reviews(id):
    """Retrieve all reviews for a specific restaurant"""
    restaurant = storage.get(Restaurant, id)
    if not restaurant:
        abort(404)
    return jsonify([review.to_dict() for review in restaurant.reviews])


@app_views.route(
    "/restaurants/<id>/reviews", methods=["POST"], strict_slashes=False
)
def create_restaurant_review(id):
    """Create a new review for a specific restaurant"""
    restaurant = storage.get(Restaurant, id)
    if not restaurant:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "client_id" not in data or "rating" not in data:
        abort(400, "Missing client_id or rating")
    data["restaurant_id"] = id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route(
    "/reviews/<review_id>", methods=["PUT"], strict_slashes=False
)
def update_review(review_id):
    """Update a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in [
            "id",
            "created_at",
            "updated_at",
            "restaurant_id",
            "client_id",
        ]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())


@app_views.route(
    "/reviews/<review_id>", methods=["DELETE"], strict_slashes=False
)
def delete_review(review_id):
    """Delete a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    return jsonify({}), 200
