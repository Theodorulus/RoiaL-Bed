import pytest
from client import client
from flask import jsonify
import json
import requests
import src.service.temperature_service as temp_serv

"""Initialize the testing environment
Creates an app for testing that has the configuration flag ``TESTING`` set to
``True``.
"""


def test_set_temperature(client):
    request = client.post("/temperature", data={"temperature": 22}, follow_redirects=True)
    res = json.loads(request.data.decode())
    assert request.status_code == 200
    assert res["status"] == "Temperature successfully recorded."


def test_set_get_temperature_service(client):
    temperature = 22
    temp_serv.set_temperature(temperature)
    res = temp_serv.get_temperature()
    assert res['value'] == temperature


def test_get_temperature(client):
    rv = client.post("/temperature", data={"temperature": 25}, follow_redirects=True)
    request = client.get("/temperature/")
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["temperature"] == 25


def test_get_temperature_realtime(client):
    request = client.get("/temperature/realtime")
    api_key = "778aeb380a12577397fc7d4e1a86a31f"
    api_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&q=Bucharest"
    response = requests.get(api_url)
    realtime_temperature = response.json()["main"]["temp"] - 272.15
    realtime_temperature = float("{:.2f}".format(realtime_temperature))
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["temperature"] == realtime_temperature
