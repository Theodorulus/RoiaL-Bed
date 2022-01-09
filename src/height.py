from flask import (
    Blueprint, request, jsonify
)
from datetime import datetime
# from auth import login_required
from db import get_db

height_bp = Blueprint('height', __name__, url_prefix='/height')

@height_bp.route('/', methods=('GET', 'POST'))
# @login_required
def set_height():
    if request.method == 'POST':
        height = request.form['height']

        if not height:
            return jsonify({'status': 'Height is required.'}), 400

        db = get_db()
        db.execute(
            'INSERT INTO heights (value)'
            'VALUES (?)',
            (height,)
        )
        db.commit()
    
    check = get_db().execute(
        'SELECT id, timestamp, value'
        'FROM heights'
        'ORDER BY timestamp DESC'
    ).fetchone()

    return jsonify({
        'status': request.method == 'POST' ? 'Height succesfully updated.' : "Height successfully retrieved.",
        'data': {
            'id': check['id'],
            'last_updated': check['timestamp'],
            'height': check['value']
        }
    }), 200