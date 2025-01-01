#!/usr/bin/env python3
"""
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api')

from api.v1.views.user_views import *
from api.v1.views.restaurant_views import *
from api.v1.views.order_views import *
