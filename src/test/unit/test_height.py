import pytest
from test.unit.client import client

"""Initialize the testing environment

Creates an app for testing that has the configuration flag ``TESTING`` set to
``True``.

"""


def test_get_height(client):
    request = client.get("/height")
    assert request.status_code == 405
