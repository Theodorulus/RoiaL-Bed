import pytest
from client import client
from flask import jsonify
import json


def test_set_sleep_stats_fail(client):
    request = client.post("/sleepstats", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['status'] == 'Duration is required.'


def test_set_sleep_stats_success(client):
    request = client.post("/sleepstats", data={"duration": 30, "rating": 6}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response["status"] == "Sleep stats successfully recorded."
    assert json.loads(request.data.decode())["data"]["rating"] == 6


def test_get_sleep_stats(client):
    client.post("/sleepstats", data={"duration": 30, "rating": 6}, follow_redirects=True)
    request = client.get("/sleepstats")
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response["status"] == "Sleep stats successfully retrieved."
    assert response["data"]["rating"] == 6


def test_get_stats_average_fail(client):
    request = client.get("/sleepstats/average")
    response = json.loads(request.data.decode())
    assert request.status_code == 404
    assert response['status'] == 'No average to calculate.'


def test_get_stats_average_success(client):
    client.post("/sleepstats", data={"duration": 20, "rating": 5}, follow_redirects=True)
    client.post("/sleepstats", data={"duration": 14, "rating": 3}, follow_redirects=True)
    request = client.get("/sleepstats/average")
    response = json.loads(request.data.decode())
    assert request.status_code == 200
    assert response["status"] == "Average rating successfully calculated."
    assert json.loads(request.data.decode())["data"]["average"] == 4
