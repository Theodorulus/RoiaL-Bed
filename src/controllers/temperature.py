from flask import (
    Blueprint, request, jsonify
)
from src.controllers.auth import login_required
import src.service.temperature_service as temp_service

temperature_bp = Blueprint('temperature', __name__, url_prefix='/temperature')


@temperature_bp.route('/', methods=['GET', 'POST'])
@login_required
def set_or_get_temperature():
    if request.method == 'POST':
        if 'temperature' not in request.form:
            return jsonify({'status': 'Temperature is required.'}), 400
        temperature = request.form['temperature']
        temp_service.set_temperature(temperature)

    check = temp_service.get_temperature()

    if check is None:
        return jsonify({
            'status': 'No temperature record found.'
        }), 404

    return jsonify({
        'status': 'Temperature successfully recorded.' if request.method == 'POST'
        else 'Temperature successfully retrieved.',
        'data': {
            'id': check['id'],
            'last_updated': check['timestamp'],
            'temperature': check['value']
        }
    }), 200
