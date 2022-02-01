import pytest 
import json
from app import start_mqtt_app, start_app
from src.models.status import Status
from paho.mqtt.client import (
    MQTT_ERR_SUCCESS,
)

@pytest.fixture
def client_mqtt():
    local_http_app = start_app()
    local_mqtt_app = start_mqtt_app(False)
    with local_http_app.test_client():
        with local_http_app.app_context():
            yield local_mqtt_app


@pytest.mark.integrationTest
def test_mqtt_status_publishing(client_mqtt):
    message = json.dumps(Status.get_status(), default=str)
    res, mid = client_mqtt.publish('smart_bed', message)
    assert res == MQTT_ERR_SUCCESS