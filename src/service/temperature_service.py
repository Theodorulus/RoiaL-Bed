from flask import (
    Blueprint, request, jsonify
)
from db import get_db
import requests

def set_temperature(temperature):
    db = get_db()
    db.execute(
        """INSERT INTO temperatures (value)
        VALUES (?)""",
        (temperature,)
    )
    db.commit()


def get_temperature():
    check = get_db().execute(
        """SELECT *
        FROM temperatures
        ORDER BY TIMESTAMP DESC
        LIMIT 1"""
    ).fetchone()

    return check
