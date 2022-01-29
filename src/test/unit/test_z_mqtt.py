import pytest 
import json
from app import start_mqtt_app, start_app
from src.models.status import Status
from paho.mqtt.client import (
    MQTT_ERR_SUCCESS,
)
import src.service.temperature_service as temp_serv
from time import sleep


@pytest.fixture
def client_mqtt():
    local_app = start_app()
    with local_app.test_client() as client:
        with local_app.app_context():
            local_mqtt_app = start_mqtt_app(False)
            yield local_mqtt_app


def test_mqtt_status_publishing(client_mqtt):
    message = "Test message"
    res, mid = client_mqtt.publish('smart_bed', message)
    assert res == MQTT_ERR_SUCCESS


def test_get_realtime_temperature_mqtt_nothing(client_mqtt):
    sleep(2)
    check = temp_serv.get_real_temperature()
    realtime_temperature = temp_serv.calculate_realtime_temperature()
    assert check["value"] == realtime_temperature
    assert "nothing" in check["status"].lower()


def test_get_realtime_temperature_mqtt_heating(client_mqtt):
    sleep(2)
    realtime_temperature = temp_serv.calculate_realtime_temperature()
    temp_serv.set_temperature(realtime_temperature + 10)
    sleep(2)
    check = temp_serv.get_real_temperature()
    assert check["value"] == realtime_temperature
    assert "heating" in check["status"].lower()


def test_get_realtime_temperature_mqtt_cooling(client_mqtt):
    sleep(2)
    realtime_temperature = temp_serv.calculate_realtime_temperature()
    temp_serv.set_temperature(realtime_temperature - 10)
    sleep(2)
    check = temp_serv.get_real_temperature()
    assert check["value"] == realtime_temperature
    assert "cooling" in check["status"].lower()
