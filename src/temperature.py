from flask import (
    Blueprint, request, jsonify
)
# from auth import login_required
from db import get_db
import requests
from src.auth import login_required

temperature_bp = Blueprint('temperature', __name__, url_prefix='/temperature')


@temperature_bp.route('/', methods=['GET', 'POST'])
@login_required
def set_temperature():
    if request.method == 'POST':
        temperature = request.form['temperature']

        if not temperature:
            return jsonify({'status': 'Temperature is required.'}), 400

        db = get_db()
        db.execute(
            """INSERT INTO temperatures (value)
            VALUES (?)""",
            (temperature,)
        )
        db.commit()

    check = get_db().execute(
        """SELECT *
        FROM temperatures
        ORDER BY TIMESTAMP DESC
        LIMIT 1"""
    ).fetchone()

    return jsonify({
        'status': 'Temperature successfully recorded.' if request.method == 'POST'
        else 'Temperature successfully retrieved.',
        'data': {
            'id': check['id'],
            'last_updated': check['timestamp'],
            'temperature': check['value']
        }
    }), 200


@temperature_bp.route('/realtime', methods=['GET'])
@login_required
def get_temperature():
    api_key = "778aeb380a12577397fc7d4e1a86a31f"

    api_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&q=Bucharest"

    response = requests.get(api_url)

    temperature = response.json()["main"]["temp"] - 272.15

    db = get_db()
    db.execute(
        """INSERT INTO temperatures (value)
        VALUES (?)""",
        (temperature,)
    )
    db.commit()

    check = get_db().execute(
        """SELECT *
        FROM temperatures
        ORDER BY TIMESTAMP DESC
        LIMIT 1"""
    ).fetchone()

    return jsonify({
        'status': 'Temperature successfully retrieved.',
        'data': {
            'id': check['id'],
            'last_updated': check['timestamp'],
            'temperature': float("{:.2f}".format(check['value']))
        }
    }), 200
