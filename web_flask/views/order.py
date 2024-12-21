#!/usr/bin/env python3
"""
"""
from views import app_views


@app_views.route('/orders', methods=['GET'], strict_slashes=False)
def all_orders_page() -> str:
    """_summary_
    """
    return 'Hello in orders page'


@app_views.route('/orders/<order>', methods=['GET'], strict_slashes=False)
def order_page(order: str) -> str:
    """_summary_
    """
    return order
