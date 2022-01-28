import pytest
from client import client
from flask import jsonify
import json

create_mode_body = {
    "mode": "test_mode",
    "height": 5,
    "temperature": 23
}


def test_create_mode_fail(client):
    request = client.post("/mode-selection/create", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['status'] == 'Mode has missing values.'


def test_create_mode_success(client):
    request = client.post("/mode-selection/create", data=create_mode_body, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert response["data"]["mode"] == create_mode_body["mode"]
    assert response["data"]["height"] == create_mode_body["height"]
    assert response["data"]["temperature"] == create_mode_body["temperature"]


def test_set_mode_fail(client):
    client.post("/mode-selection/create", data=create_mode_body, follow_redirects=True)
    request = client.post("/mode-selection", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['status'] == 'Mode is required.'


def test_set_mode_success(client):
    client.post("/mode-selection/create", data=create_mode_body, follow_redirects=True)
    request = client.post("/mode-selection", data={"mode": "test_mode"}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert response["data"]["mode"] == create_mode_body["mode"]
    assert response["data"]["height"] == create_mode_body["height"]
    assert response["data"]["temperature"] == create_mode_body["temperature"]


def test_get_selected_mode(client):
    client.post("/mode-selection/create", data=create_mode_body, follow_redirects=True)
    client.post("/mode-selection", data={"mode": "test_mode"}, follow_redirects=True)
    request = client.get("/mode-selection")
    response = json.loads(request.data.decode())
    assert response["data"]["mode"] == create_mode_body["mode"]
    assert response["data"]["height"] == create_mode_body["height"]
    assert response["data"]["temperature"] == create_mode_body["temperature"]
