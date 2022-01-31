from flask import (
    Blueprint, request, jsonify
)
from datetime import datetime, timedelta
from src.controllers.auth import login_required
from db import get_db
import random

sleep_stats_bp = Blueprint('sleep_stats', __name__, url_prefix='/sleepstats')


@sleep_stats_bp.route('/', methods=['GET', 'POST'])
@login_required
def get_stats():
    if request.method == 'POST':
        if 'duration' not in request.form:
            return jsonify({'status': 'Duration is required'}), 400

        if 'rating' not in request.form:
            return jsonify({'status': 'Rating is required'}), 400

        duration = int(request.form['duration'])
        rating = request.form['rating']
        start_time = datetime.fromtimestamp(datetime.now().timestamp() - duration).replace(microsecond=0)

        db = get_db()

        # Manually insert data
        db.execute(
            """INSERT INTO sleep_stats (start, end, rating)
            VALUES (?, CURRENT_TIMESTAMP, ?)""",
            (start_time, rating, )
        )

        db.commit()

    check = get_db().execute(
        """SELECT *
        FROM sleep_stats
        WHERE rating != 0
        ORDER BY end DESC
        LIMIT 1"""
    ).fetchone()

    if check is None:
        return jsonify({'status': "No stats to retrieve."}), 400

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


def rate_sleep():
    chance = random.randint(0, 5)
    first_alarm = get_first_alarm()
    db = get_db()

    stats = get_db().execute(
        """SELECT *
        FROM sleep_stats
        WHERE rating = 0
        ORDER BY start DESC
        LIMIT 1"""
    ).fetchone()

    # Go to sleep
    if chance == 5:
        if not stats:
            db.execute(
                """INSERT INTO sleep_stats (start, end, rating)
                VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)""",
                (0,)
            )
            db.commit()

    # Wake up
    elif stats:
        if chance == 0 or (first_alarm and first_alarm["start"] == datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
            db.execute("UPDATE sleep_stats SET end = CURRENT_TIMESTAMP WHERE id = ?", (stats['id'],))
            rating = get_rating()
            db.execute("UPDATE sleep_stats SET rating = ? WHERE id = ?", (rating, stats['id'],))
            db.commit()


def get_rating():
    # based on different factors return a rating
    return random.randint(1, 10)


def get_first_alarm():
    check = get_db().execute(
        """SELECT *
        FROM alarms
        WHERE start > CURRENT_TIMESTAMP
        ORDER BY start
        LIMIT 1"""
    ).fetchone()

    return check
