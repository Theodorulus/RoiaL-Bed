from flask import (
    Blueprint, request, jsonify
)
from datetime import datetime, timedelta
from src.controllers.auth import login_required
import src.service.sleep_stats_service as stats_service

sleep_stats_bp = Blueprint('sleep_stats', __name__, url_prefix='/sleepstats')


@sleep_stats_bp.route('/', methods=['GET', 'POST'])
@login_required
def get_stats():
    if request.method == 'POST':
        # Manually insert data

        if 'duration' not in request.form:
            return jsonify({'status': 'Duration is required.'}), 400

        if 'rating' not in request.form:
            return jsonify({'status': 'Rating is required.'}), 400

        duration = int(request.form['duration'])
        rating = request.form['rating']
        start_time = datetime.fromtimestamp(datetime.utcnow().timestamp() - duration).replace(microsecond=0)
        stats_service.set_sleep_stats(start_time, rating)

    check = stats_service.get_last_complete_sleep()

    if check is None:
        return jsonify({'status': "No stats to retrieve."}), 404

    return jsonify({
        'status': 'Sleep stats successfully recorded.' if request.method == 'POST'
        else "Sleep stats successfully retrieved.",
        'data': {
            'id': check['id'],
            'start': check['start'],
            'end': check['end'],
            'rating': check['rating']
        }
    }), 200


@sleep_stats_bp.route('/average/', methods=['GET'])
@login_required
def get_stats_average():
    check = stats_service.get_average_rating()

    if check['average'] is None:
        return jsonify({'status': "No average to calculate."}), 404

    return jsonify({
        'status': "Average rating successfully calculated.",
        'data': {
            'average': check['average']
        }
    }), 200
