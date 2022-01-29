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


def update_realtime_temperature():
    realtime_temperature = calculate_realtime_temperature()

    db = get_db()
    user_temperature = get_user_temperature()
    temperature_status = ""
    if user_temperature is None or user_temperature['value'] == realtime_temperature:
        temperature_status = "Doing nothing"
    elif user_temperature['value'] < realtime_temperature:
        do_cooling()
        temperature_status = "Cooling"
    else:
        do_heating()
        temperature_status = "Heating"

    db.execute(
        """INSERT INTO real_temperatures (value, status)
        VALUES (?,?)""",
        (realtime_temperature, temperature_status,)
    )
    db.commit()


def get_user_temperature():
    check = get_db().execute(
        """SELECT *
        FROM temperatures
        ORDER BY TIMESTAMP DESC
        LIMIT 1"""
    ).fetchone()

    return check


def get_real_temperature():
    check = get_db().execute(
        """SELECT *
        FROM real_temperatures
        ORDER BY TIMESTAMP DESC
        LIMIT 1"""
    ).fetchone()

    return check

def calculate_realtime_temperature():
    api_key = "778aeb380a12577397fc7d4e1a86a31f"
    api_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&q=Bucharest"
    response = requests.get(api_url)
    realtime_temperature = response.json()["main"]["temp"] - 272.15
    realtime_temperature = float("{:.2f}".format(realtime_temperature))
    return realtime_temperature

def do_cooling():
    # Some algorithm to cool the bed
    print("Cooling the bed")

def do_heating():
    # Some algorithm to heat the bed
    print("Heating the bed")
