from flask import (
    Blueprint, request, jsonify
)
from src.controllers.auth import login_required
from db import get_db

height_bp = Blueprint('height', __name__, url_prefix='/height')


@height_bp.route('/', methods=['GET', 'POST'])
@login_required
def set_height():
    if request.method == 'POST':
        if 'height' not in request.form:
            return jsonify({'status': 'Height is required.'}), 400

        height = request.form['height']

        db = get_db()
        db.execute(
            """INSERT INTO heights (value)
            VALUES (?)""",
            (height,)
        )
        db.commit()
    
    check = get_db().execute(
        """SELECT *
        FROM heights
        ORDER BY TIMESTAMP DESC
        LIMIT 1"""
    ).fetchone()

    return jsonify({
        'status': 'Height succesfully updated.' if request.method == 'POST' else "Height successfully retrieved.",
        'data': {
            'id': check['id'],
            'last_updated': check['timestamp'],
            'height': check['value']
        }
    }), 200
