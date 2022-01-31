import pytest
from client import client
from flask import jsonify
import json
import requests
import src.service.music_service as music_service


def test_add_song(client):
    request = client.post('/music/add', data={"song_path": "Song_Path_Example"}, follow_redirects=True)
    res = json.loads(request.data.decode())
    assert request.status_code == 200
    assert res["status"] == 'Song added.'


def test_play_song_index(client):
    client.post('/music/add', data={"song_path": "Song_Path_Example"}, follow_redirects=True)
    request = client.get("/music/play/1/")
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["id"] == 1


def test_play_song_path(client):
    client.post('/music/add', data={"song_path": "Song_Path_Example"}, follow_redirects=True)
    request = client.get("/music/play/Song_Path_Example/")
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["path"] == 'Song_Path_Example'


def test_add_alarm(client):
    client.post('/music/add', data={"song_path": "Song_Path_Example"}, follow_redirects=True)
    request = client.post('/music/setalarm', data={"start": "2022-01-23 12:00:00", "song_id": "1"}, follow_redirects=True)
    res = json.loads(request.data.decode())
    assert request.status_code == 200
    assert res["status"] == 'Added alarm.'


def test_add_song_400(client):
    request = client.post("/music/add", data={}, follow_redirects=True)
    res = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "Path is required." in res["status"]


def test_play_song_empty_db(client):
    request = client.get("/music/play/x")
    assert request.status_code == 404
    assert "Could not find song." in json.loads(request.data.decode())["status"]

    
def test_set_get_user_temperature_service(client):
    music_service.add_music_to_db("path")
    res = music_service.get_last_song()
    assert res['song_path'] == "path"