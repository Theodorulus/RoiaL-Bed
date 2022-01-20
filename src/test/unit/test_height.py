import pytest
from client import client
from flask import jsonify
import json

"""Initialize the testing environment

Creates an app for testing that has the configuration flag ``TESTING`` set to
``True``.

"""


def test_get_height(client):
    rv = client.post("/height", data={"height": 10}, follow_redirects=True)
    request = client.get("/height")
    # assert request.status_code == 405
    assert request.status_code == 200
    assert json.loads(request.data.decode())["data"]["height"] == 10
