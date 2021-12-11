
from flask import Flask
from flask_mqtt import Mqtt
from threading import Thread
import json
import time
import src.models.status as status
from src.example_endpoint import example_endpoint


app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

# register blueprints
app.register_blueprint(example_endpoint)

mqtt = Mqtt(app)
    
# fucntion for mqtt's thread    
def background_thread():
    while True:
        time.sleep(1)
        message = json.dumps(status.get_status(), default=str)
        mqtt.publish('smart_bed', message)

def init_mqtt_thread():
    thread = Thread(target=background_thread)
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    init_mqtt_thread()
    app.run()