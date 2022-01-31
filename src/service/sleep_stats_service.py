from flask import (
    Blueprint, request, jsonify
)
from db import get_db
import requests
import random


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


def get_upcoming_alarm():
    check = get_db().execute(
        """SELECT *
        FROM alarms
        WHERE start > CURRENT_TIMESTAMP
        ORDER BY start
        LIMIT 1"""
    ).fetchone()

    return check
