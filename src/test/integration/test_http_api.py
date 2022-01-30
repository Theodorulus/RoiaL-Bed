import pytest
from src.test.unit.client import client
from flask import jsonify
import json

@pytest.mark.integrationTest
def test_set_alarm(client):
    song_request = client.post("/music/add", data={"song_path": "./song.mp3"}, follow_redirects=True)
    alarm_request = client.post("/music/setalarm", data={"song_id": "1", "start": "2023-01-30 12:00:00"}, follow_redirects=True)
    assert song_request.status_code == 200 and alarm_request.status_code == 200
    assert json.loads(alarm_request.data.decode())["status"] == "Added alarm."