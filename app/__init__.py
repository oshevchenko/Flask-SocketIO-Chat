from flask import Flask
from flask_socketio import SocketIO
from flask_mqtt import Mqtt


class MqttSocketIO(Mqtt):
    mqtt_room_name = 'mqtt_room'
    total_mqtt = 0


mqtt = MqttSocketIO()
socketio = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_REFRESH_TIME'] = 1.0
    app.secret_key = '4ce2134367cf4025b6dfb7f7fa5315dd'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    mqtt.init_app(app)

    return app

