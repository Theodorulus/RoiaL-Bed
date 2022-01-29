import pytest 
import json
from app import start_mqtt_app, start_app
from src.models.status import Status
from paho.mqtt.client import (
    MQTT_ERR_SUCCESS,
)


@pytest.fixture
def client_mqtt():
    start_app()
    local_mqtt_app = start_mqtt_app(False)
    yield local_mqtt_app


def test_mqtt_status_publishing(client_mqtt):
    message = "Test message"
    res, mid = client_mqtt.publish('smart_bed', message)
    assert res == MQTT_ERR_SUCCESS
