from flask import (
    Blueprint, request, jsonify
)
from datetime import datetime
# from auth import login_required
from db import get_db

mode_bp = Blueprint('mode_selection', __name__, url_prefix='/mode-selection')


@mode_bp.route('/', methods=('GET', 'POST'))
# @login_required
def select_mode():
    if request.method == 'POST':
        mode = request.form['mode']

        if not mode:
            return jsonify({'status': 'Mode is required.'}), 400

        db = get_db()
        check = get_db().execute(
            'SELECT id, value, height, temperature'
            'FROM modes'
            'WHERE value = ?',
            (mode,)
        ).fetchone()
        if not check:
            return jsonify({'status': 'Mode is not valid.'}), 400

        db.execute(
            'UPDATE modes'
            'SET active = 0'
            'WHERE active = 1'
        )
        db.execute(
            'UPDATE modes'
            'SET active = 1'
            'WHERE value = ?',
            (mode,)
        )
        # set other features to some default values depending on the mode
        db.execute(
            'INSERT INTO heights (value)'
            'VALUES (?)',
            (check['height'],)
        )
        db.execute(
            'INSERT INTO temperatures (value)'
            'VALUES (?)',
            (check['temperature'],)
        )
        # other
        db.commit()

    check = get_db().execute(
        'SELECT id, value, height, temperature'
        'FROM modes'
        'WHERE active = 1'
    ).fetchone()

    return jsonify({
        'status': 'Mode successfully selected.' if request.method == 'POST' else 'Mode successfully retrieved.',
        'data': {
            'id': check['id'],
            'mode': check['value'],
            'height': check['height'],
            'temperature': check['temperature']
        }
    }), 200


@mode_bp.route('/create', methods='POST')
# @login_required
def create_mode():
    mode = request.form['mode']
    height = request.form['height']
    temperature = request.form['temperature']

    if not mode or not height or not temperature:
        return jsonify({'status': 'Mode has missing values.'}), 400

    db.execute(
        'INSERT INTO modes (value, height, temperature)'
        'VALUES (?, ?, ?)',
        (mode, height, temperature,)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, value, height, temperature'
        'FROM modes'
        'ORDER BY timestamp DESC'
    ).fetchone()

    return jsonify({
        'status': 'Mode successfully added.',
        'data': {
            'id': check['id'],
            'mode': check['value'],
            'height': check['height'],
            'temperature': check['temperature']
        }
    }), 200
