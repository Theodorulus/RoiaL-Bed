from flask import (
    Blueprint, request, jsonify
)
# from auth import login_required
from db import get_db
from src.controllers.auth import login_required
import src.service.mode_selection_service as mode_service
import src.service.height_service as height_service
import src.service.temperature_service as temp_service

mode_bp = Blueprint('mode_selection', __name__, url_prefix='/mode-selection')


@mode_bp.route('/', methods=['GET', 'POST'])
@login_required
def select_mode():
    if request.method == 'POST':
        if 'mode' not in request.form:
            return jsonify({'status': 'Mode is required.'}), 400

        mode = request.form['mode']

        check = mode_service.get_mode_by_name(mode)
        if not check:
            return jsonify({'status': 'Mode is not valid.'}), 400

        mode_service.set_active_mode(mode)

        # set other features to some default values depending on the mode
        height_service.set_height(check['height'])
        temp_service.set_temperature(check['temperature'])

    check = mode_service.get_active_mode()

    return jsonify({
        'status': 'Mode successfully selected.' if request.method == 'POST' else 'Mode successfully retrieved.',
        'data': {
            'id': check['id'],
            'mode': check['value'],
            'height': check['height'],
            'temperature': check['temperature']
        }
    }), 200


@mode_bp.route('/create', methods=['POST'])
@login_required
def create_mode():
    if 'mode' not in request.form or 'height' not in request.form or 'temperature' not in request.form:
        return jsonify({'status': 'Mode has missing values.'}), 400

    mode = request.form['mode']
    height = request.form['height']
    temperature = request.form['temperature']

    mode_service.create_mode(mode, height, temperature)

    check = mode_service.get_last_created_mode()

    return jsonify({
        'status': 'Mode successfully added.',
        'data': {
            'id': check['id'],
            'mode': check['value'],
            'height': check['height'],
            'temperature': check['temperature']
        }
    }), 200
