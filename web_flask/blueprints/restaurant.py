#!/usr/bin/env python3
"""
"""
from views import app_views


@app_views.route('/restaurants', methods=['GET'], strict_slashes=False)
def all_restaurants_page() -> str:
    """_summary_
    """
    return 'Hello in restaurants page'


@app_views.route('/restaurants/<rest>', methods=['GET'], strict_slashes=False)
def restaurant_page(rest: str) -> str:
    """_summary_
    """
    return rest
