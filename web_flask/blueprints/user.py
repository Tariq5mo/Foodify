#!/usr/bin/env python3
"""
"""
from views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users_page() -> str:
    """_summary_
    """
    return 'Hello in users page'


@app_views.route('/users/<user>', methods=['GET'], strict_slashes=False)
def user_page(user: str) -> str:
    """_summary_
    """
    return user
