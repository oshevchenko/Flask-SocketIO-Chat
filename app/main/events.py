from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from .. import mqtt


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    if room == mqtt.mqtt_room_name:
        mqtt.total_mqtt += 1
        print('Join total_mqtt=' + str(mqtt.total_mqtt))
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)
    mqtt.publish('4ce213436/mytopic', session.get('name') + ':' + message['msg'])


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    if room == mqtt.mqtt_room_name:
        mqtt.total_mqtt -= 1
        print('Quit total_mqtt=' + str(mqtt.total_mqtt))
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('4ce213436/mytopic')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    # print('received args: ' + message.topic)
    if mqtt.total_mqtt > 0:
        socketio.emit('mqtt_message', {'msg': message.topic + ' < ' + message.payload.decode()}, namespace='/chat', room=mqtt.mqtt_room_name)

