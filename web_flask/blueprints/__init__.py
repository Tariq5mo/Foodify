#!/usr/bin/env python3
"""
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__)

from views.welcome import *
from views.restaurant import *
from views.user import *
from views.order import *
