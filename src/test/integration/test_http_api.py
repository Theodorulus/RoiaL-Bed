import pytest
from src.test.unit.client import client
from flask import jsonify
import json


create_mode_body = {
    "mode": "test_mode",
    "height": 5,
    "temperature": 23
}

@pytest.mark.integrationTest
def test_set_alarm(client):
    song_request = client.post("/music/add", data={"song_path": "./song.mp3"}, follow_redirects=True)
    alarm_request = client.post("/music/setalarm", data={"song_id": "1", "start": "2023-01-30 12:00:00"}, follow_redirects=True)
    assert song_request.status_code == 200 and alarm_request.status_code == 200
    assert json.loads(alarm_request.data.decode())["status"] == "Added alarm."
    
@pytest.mark.integrationTest
def test_set_alarm_fail(client):
    song_request = client.post("/music/add", data={"song_path": "./song.mp3"}, follow_redirects=True)
    alarm_request = client.post("/music/setalarm", data={"song_id": "2", "start": "2023-01-30 12:00:00"}, follow_redirects=True)
    assert song_request.status_code == 200 and alarm_request.status_code == 404
    assert json.loads(alarm_request.data.decode())["status"] == "record not found."

@pytest.mark.integrationTest  
def test_set_mode_fail(client):
    client.post("/mode-selection/create", data=create_mode_body, follow_redirects=True)
    request = client.post("/mode-selection", data={}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert request.status_code == 400
    assert response['status'] == 'Mode is required.'

@pytest.mark.integrationTest
def test_set_mode_success(client):
    client.post("/mode-selection/create", data=create_mode_body, follow_redirects=True)
    request = client.post("/mode-selection", data={"mode": "test_mode"}, follow_redirects=True)
    response = json.loads(request.data.decode())
    assert response["data"]["mode"] == create_mode_body["mode"]
    assert response["data"]["height"] == create_mode_body["height"]
    assert response["data"]["temperature"] == create_mode_body["temperature"]

@pytest.mark.integrationTest
def test_get_selected_mode_success(client):
    client.post("/mode-selection/create", data=create_mode_body, follow_redirects=True)
    client.post("/mode-selection", data={"mode": "test_mode"}, follow_redirects=True)
    request = client.get("/mode-selection")
    response = json.loads(request.data.decode())
    assert response["data"]["mode"] == create_mode_body["mode"]
    assert response["data"]["height"] == create_mode_body["height"]
    assert response["data"]["temperature"] == create_mode_body["temperature"]

@pytest.mark.integrationTest
def test_play_song_index(client):
    client.post('/music/add', data={"song_path": "Song_Path_Example"}, follow_redirects=True)
    request = client.get("/music/play/1/")
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["id"] == 1

@pytest.mark.integrationTest
def test_play_song_path(client):
    client.post('/music/add', data={"song_path": "Song_Path_Example"}, follow_redirects=True)
    request = client.get("/music/play/Song_Path_Example/")
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["path"] == 'Song_Path_Example'

@pytest.mark.integrationTest
def test_add_alarm(client):
    client.post('/music/add', data={"song_path": "Song_Path_Example"}, follow_redirects=True)
    request = client.post('/music/setalarm', data={"start": "2022-01-23 12:00:00", "song_id": "1"}, follow_redirects=True)
    res = json.loads(request.data.decode())
    assert request.status_code == 200
    assert res["status"] == 'Added alarm.'
    