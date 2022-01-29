import pytest
from client import client
from flask import jsonify
import json
import src.service.height_service as height_service


def test_set_height_fail(client):
    request = client.post("/height", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['status'] == 'Height is required.'


def test_set_height_success(client):
    request = client.post("/height", data={"height": 15}, follow_redirects=True)
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["height"] == 15


def test_get_height(client):
    client.post("/height", data={"height": 10}, follow_redirects=True)
    request = client.get("/height")
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["height"] == 10


def test_get_set_height(client):
    height = 11
    height_service.set_height(height)
    check = height_service.get_height()
    assert check['value'] == height