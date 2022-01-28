import pytest
from client import client
from flask import jsonify
import json
import requests


def test_add_song(client):
    request = client.post('/music/add', data={"song_path": "Song_Path_Example"}, follow_redirects=True)
    res = json.loads(request.data.decode())
    assert request.status_code == 200
    assert res["status"] == 'Added song.'


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
    request = client.post('/music/setalarm', data={"start": "2022-01-23 12:00", "song_id": "1"}, follow_redirects=True)
    res = json.loads(request.data.decode())
    assert request.status_code == 200
    assert res["status"] == 'Added alarm.'


