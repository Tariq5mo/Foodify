#!/usr/bin/env python3
"""
"""
from views import app_views


@app_views.route('/', methods=['GET'], strict_slashes=False)
def welcome_page() -> str:
    """_summary_
    """
    return 'Hello in welcome page'
