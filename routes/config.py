from flask import Blueprint, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

config_routes = Blueprint('config', __name__)


@config_routes.route('/api/v1/config')
def get_config():
    api_key = os.getenv('TOMTOM_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not found'}), 500
    return jsonify({'TOMTOM_API_KEY': api_key})
