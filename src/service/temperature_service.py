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


def set_temperature_realtime():
    api_key = "778aeb380a12577397fc7d4e1a86a31f"
    api_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&q=Bucharest"
    response = requests.get(api_url)
    temperature = response.json()["main"]["temp"] - 272.15
    temperature = float("{:.2f}".format(temperature))
    set_temperature(temperature)


def get_temperature():
    check = get_db().execute(
        """SELECT *
        FROM temperatures
        ORDER BY TIMESTAMP DESC
        LIMIT 1"""
    ).fetchone()

    return check


