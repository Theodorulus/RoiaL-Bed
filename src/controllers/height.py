from flask import (
    Blueprint, request, jsonify
)
from src.controllers.auth import login_required
import src.service.height_service as height_service

height_bp = Blueprint('height', __name__, url_prefix='/height')


@height_bp.route('/', methods=['GET', 'POST'])
@login_required
def set_height():
    if request.method == 'POST':
        if 'height' not in request.form:
            return jsonify({'status': 'Height is required.'}), 400
        height = request.form['height']

        height_service.set_height(height)
    
    check = height_service.get_height()

    return jsonify({
        'status': 'Height succesfully updated.' if request.method == 'POST' else "Height successfully retrieved.",
        'data': {
            'id': check['id'],
            'last_updated': check['timestamp'],
            'height': check['value']
        }
    }), 200
