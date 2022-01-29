import pytest
from client import client
from flask import jsonify
import json
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


def test_set_get_user_temperature_service(client):
    temp_serv.set_temperature(temperature)
    res = temp_serv.get_user_temperature()
    assert res['value'] == temperature


def test_get_user_temperature_not_found(client):
    request = client.get("/temperature/")
    assert request.status_code == 404
    assert "no temperature record found" in json.loads(request.data.decode())["status"].lower()


def test_get_user_temperature(client):
    client.post("/temperature", data={"temperature": temperature}, follow_redirects=True)
    request = client.get("/temperature/")
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["temperature"] == temperature


def test_set_get_realtime_temperature_service(client):
    realtime_temperature = temp_serv.calculate_realtime_temperature()

    temp_serv.update_realtime_temperature()
    res = temp_serv.get_real_temperature()
    assert res['value'] == realtime_temperature


def test_get_real_temperature_not_found(client):
    request = client.get("/temperature/real")
    assert request.status_code == 404
    assert "no realtime temperature record found" in json.loads(request.data.decode())["status"].lower()


def test_get_real_temperature(client):
    realtime_temperature = temp_serv.calculate_realtime_temperature()

    temp_serv.update_realtime_temperature()
    request = client.get("/temperature/real")
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["temperature"] == realtime_temperature
