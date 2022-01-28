import pytest
from client import client
from flask import jsonify
import json
import requests
import src.service.temperature_service as temp_serv

temperature = 22


def test_set_temperature(client):
    request = client.post("/temperature", data={"temperature": temperature}, follow_redirects=True)
    res = json.loads(request.data.decode())
    assert request.status_code == 200
    assert res["status"] == "Temperature successfully recorded."
    assert res["data"]["temperature"] == temperature


def test_set_temperature_400(client):
    request = client.post("/temperature", data={}, follow_redirects=True)
    res = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "temperature is required" in res["status"].lower()


def test_set_get_temperature_service(client):
    temp_serv.set_temperature(temperature)
    res = temp_serv.get_temperature()
    assert res['value'] == temperature


def test_get_temperature_not_found(client):
    request = client.get("/temperature/")
    assert request.status_code == 404
    assert "no temperature record found" in json.loads(request.data.decode())["status"].lower()


def test_get_temperature(client):
    client.post("/temperature", data={"temperature": temperature}, follow_redirects=True)
    request = client.get("/temperature/")
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["temperature"] == temperature


def test_set_get_realtime_temperature(client):
    temp_serv.set_temperature_realtime()
    request = client.get("/temperature")
    api_key = "778aeb380a12577397fc7d4e1a86a31f"
    api_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&q=Bucharest"
    response = requests.get(api_url)
    realtime_temperature = response.json()["main"]["temp"] - 272.15
    realtime_temperature = float("{:.2f}".format(realtime_temperature))
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["temperature"] == realtime_temperature


def test_set_get_realtime_temperature_service(client):
    api_key = "778aeb380a12577397fc7d4e1a86a31f"
    api_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&q=Bucharest"
    response = requests.get(api_url)
    realtime_temperature = response.json()["main"]["temp"] - 272.15
    realtime_temperature = float("{:.2f}".format(realtime_temperature))

    temp_serv.set_temperature_realtime()
    res = temp_serv.get_temperature()
    assert res['value'] == realtime_temperature
