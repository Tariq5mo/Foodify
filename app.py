#!/usr/bin/env python3
"""The Foodify app
"""
from flask import Flask
from web_flask.api.v1.views import app_views

foodify_app: Flask = Flask(__name__, template_folder='web_flask/templates', static_folder='web_flask/static')
foodify_app.register_blueprint(app_views, url_prefix='/api')


if __name__ == "__main__":
    foodify_app.run(debug=True)
