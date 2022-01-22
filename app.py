from flask import Flask
from flask_mqtt import Mqtt
from threading import Thread
import json
import time
import db
import src.models.status as status
from src.example_endpoint import example_endpoint
from src.height import height_bp
from src.mode_selection import mode_bp
from src.temperature import temperature_bp
from src.music import music_bp
from src.auth import auth_bp

app = None
mqtt = None


def start_app():
    global app, mqtt
    app = Flask(__name__)
    app.config['MQTT_BROKER_URL'] = 'localhost'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 5
    app.config['MQTT_TLS_ENABLED'] = False

    app.config.from_mapping(SECRET_KEY='shhhhhh',)
    app.url_map.strict_slashes = False

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(example_endpoint)
    app.register_blueprint(height_bp)
    app.register_blueprint(mode_bp)
    app.register_blueprint(temperature_bp)
    app.register_blueprint(music_bp)
    mqtt = Mqtt(app)

    with app.app_context():
        db.init_app(app)

    return app


# function for mqtt's thread    
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
    app = start_app()
    init_mqtt_thread()
    app.run()
