from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from models import storage
from models.client import Client

delivery_routes = Blueprint('delivery_routes', __name__)

@delivery_routes.route('/delivery')
@login_required
def delivery_page():
    """Render delivery location page"""
    try:
        with storage.session_scope() as session:
            client = session.query(Client).get(current_user.id)
            stored_location = {
                'address': client.address if client.address else None,
                'lat': float(client.latitude) if client.latitude else None,
                'lng': float(client.longitude) if client.longitude else None
            } if client.address else None

            return render_template('delivery.html',
                                 stored_location=stored_location)
    except Exception as e:
        print(f"Error loading delivery page: {e}")
        return render_template('delivery.html', stored_location=None)

@delivery_routes.route('/api/v1/location/save', methods=['POST'])
@login_required
def save_location():
    """Save delivery location"""
    try:
        data = request.get_json()

        with storage.session_scope() as session:
            client = session.query(Client).get(current_user.id)
            client.latitude = data['lat']
            client.longitude = data['lng']
            client.address = data['address']
            client.phone = data['phone']
            client.delivery_instructions = data.get('instructions', '')

            session.commit()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500