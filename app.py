from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import time
import telnet_scraper
from actions import DatabaseActions
import os
import json
from datetime import datetime

SERVER_MAC_ADDRESS = '70:18:8b:ae:e3:6b'
IMAGE_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
socketio = SocketIO(app)
db_actions = DatabaseActions()

@app.route('/')
def show_table():
    green_led = os.path.join(IMAGE_FOLDER, 'green_led.jpg')
    red_led = os.path.join(IMAGE_FOLDER, 'red_led.jpg')
    current_time = datetime.now().strftime('%I:%M %p, %A, %x')
    return render_template('index.html', green_led=green_led, red_led=red_led)


def loop_device_scan():
    telnet_session = telnet_scraper.start_telnet_session()
    while True:
        device_dict = telnet_scraper.get_devices(telnet_session)
        db_actions.process_device_dict(device_dict)
        send_update()
        #send_update_test()
        time.sleep(60)


@socketio.on('connect')
def send_update():
    watched_devices = db_actions.query_watched_devices()
    watched_devices_list = []

    for device in watched_devices:
        device_details_dict = {'Connected': device.connected, 'Nickname': device.nickname}
        watched_devices_list.append({device.mac_address: device_details_dict})

    socketio.emit('json', json.dumps(watched_devices_list))

    update_time = datetime.now()

    # Formatting example 09:42PM, Tuesday, 03/19/19
    socketio.emit('update time', update_time.strftime('%I:%M %p, %A, %x'))

def send_update_test():
    watched_devices = db_actions.query_watched_devices()
    watched_devices_list = []

    for device in watched_devices:
        device_details_dict = {'Connected': False, 'Nickname': device.nickname}
        watched_devices_list.append({device.mac_address: device_details_dict})

    socketio.emit('json', json.dumps(watched_devices_list))
    socketio.emit('update time', 'All disconnected!!!')

    watched_devices_list.clear()

    time.sleep(5)

    for device in watched_devices:
        device_details_dict = {'Connected': True, 'Nickname': device.nickname}
        watched_devices_list.append({device.mac_address: device_details_dict})

    socketio.emit('json', json.dumps(watched_devices_list))
    socketio.emit('update time', 'All connected!!!')

    time.sleep(5)

    watched_devices_list.clear()

    for device in watched_devices:
        device_details_dict = {'Connected': device.connected, 'Nickname': device.nickname}
        watched_devices_list.append({device.mac_address: device_details_dict})

    update_time = datetime.now()
    socketio.emit('json', json.dumps(watched_devices_list))
    socketio.emit('update time', update_time.strftime('%I:%M %p, %A, %x'))


if __name__ == '__main__':
    process = Thread(target=loop_device_scan)
    process.start()
    socketio.run(app=app, host='0.0.0.0', debug=False, port=8000)


