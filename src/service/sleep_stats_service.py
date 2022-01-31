from flask import (
    Blueprint, request, jsonify
)
from db import get_db
import random
from datetime import datetime
from src.service.music_service import get_upcoming_alarm


def set_sleep_stats(start_time, rating):
    db = get_db()

    db.execute(
        """INSERT INTO sleep_stats (start, end, rating)
        VALUES (?, CURRENT_TIMESTAMP, ?)""",
        (start_time, rating, )
    )

    db.commit()


def get_last_complete_sleep():
    check = get_db().execute(
        """SELECT *
        FROM sleep_stats
        WHERE rating != 0
        ORDER BY end DESC
        LIMIT 1"""
    ).fetchone()

    return check


def get_last_incomplete_sleep():
    check = get_db().execute(
        """SELECT *
        FROM sleep_stats
        WHERE rating = 0
        ORDER BY start DESC
        LIMIT 1"""
    ).fetchone()

    return check


def get_rating():
    # based on different factors return a rating
    return random.randint(1, 10)


def get_average_rating():
    check = get_db().execute(
        """SELECT ROUND(AVG(rating), 2) AS average
        FROM sleep_stats
        WHERE rating != 0"""
    ).fetchone()

    return check


def sleep_cycle():
    chance = random.randint(0, 5)
    first_alarm = get_upcoming_alarm()
    db = get_db()

    stats = get_last_incomplete_sleep()

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
        if chance == 0 or (first_alarm and first_alarm["start"] == datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")):
            db.execute("UPDATE sleep_stats SET end = CURRENT_TIMESTAMP WHERE id = ?", (stats['id'],))
            rating = get_rating()
            db.execute("UPDATE sleep_stats SET rating = ? WHERE id = ?", (rating, stats['id'],))
            db.commit()
