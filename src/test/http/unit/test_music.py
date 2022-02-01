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

def test_add_song_400(client):
    request = client.post("/music/add", data={}, follow_redirects=True)
    res = json.loads(request.data.decode())
    assert request.status_code == 400
    assert "Path is required." in res["status"]


def test_play_song_empty_db(client):
    request = client.get("/music/play/x")
    assert request.status_code == 404
    assert "Could not find song." in json.loads(request.data.decode())["status"]

    
def test_get_last_song(client):
    music_service.add_music_to_db("path")
    res = music_service.get_last_song()
    assert res['song_path'] == "path"