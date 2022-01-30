import pytest
from client import client
from flask import jsonify
import json
import src.service.mode_selection_service as mode_service


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


def test_get_selected_mode_success(client):
    client.post("/mode-selection/create", data=create_mode_body, follow_redirects=True)
    client.post("/mode-selection", data={"mode": "test_mode"}, follow_redirects=True)
    request = client.get("/mode-selection")
    response = json.loads(request.data.decode())
    assert response["data"]["mode"] == create_mode_body["mode"]
    assert response["data"]["height"] == create_mode_body["height"]
    assert response["data"]["temperature"] == create_mode_body["temperature"]


def test_get_selected_mode_fail(client):
    request = client.get("/mode-selection")
    assert request.status_code == 404
    assert json.loads(request.data.decode())["status"] == "No mode record found."


def test_create_get_mode(client):
    mode_service.create_mode(create_mode_body['mode'], create_mode_body["height"], create_mode_body["temperature"])
    mode_by_last = mode_service.get_last_created_mode()
    mode_by_name = mode_service.get_mode_by_name(create_mode_body['mode'])
    assert mode_by_last['value'] == create_mode_body["mode"]
    assert mode_by_last['height'] == create_mode_body["height"]
    assert mode_by_last['temperature'] == create_mode_body["temperature"]
    assert mode_by_name['value'] == create_mode_body["mode"]
    assert mode_by_name['height'] == create_mode_body["height"]
    assert mode_by_name['temperature'] == create_mode_body["temperature"]


def test_set_get_active_mode(client):
    mode_service.create_mode(create_mode_body['mode'], create_mode_body["height"], create_mode_body["temperature"])
    mode_service.set_active_mode(create_mode_body['mode'])
    mode = mode_service.get_active_mode()
    assert mode['value'] == create_mode_body["mode"]
    assert mode['height'] == create_mode_body["height"]
    assert mode['temperature'] == create_mode_body["temperature"]