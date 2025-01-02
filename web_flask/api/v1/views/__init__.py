from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api")

from web_flask.api.v1.error_handlers import *
from web_flask.api.v1.views.client_views import *
from web_flask.api.v1.views.index import *
from web_flask.api.v1.views.menu_items_views import *
from web_flask.api.v1.views.index import *
from web_flask.api.v1.views.restaurant_views import *
from web_flask.api.v1.views.index import *
