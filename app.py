from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import time
import telnet_scraper
from actions import DatabaseActions

SERVER_MAC_ADDRESS = '70:18:8b:ae:e3:6b'

app = Flask(__name__)
socketio = SocketIO(app)
db_actions = DatabaseActions()

@app.route('/')
def show_table():
    return render_template('index.html',
                           connected_devices=db_actions.query_watched_devices())


def loop_device_scan():
    telnet_session = telnet_scraper.start_telnet_session()
    while True:
        device_dict = telnet_scraper.get_devices(telnet_session)
        db_actions.process_device_dict(device_dict)
        connected_devices = db_actions.query_connected_devices(ignore_device_list=[SERVER_MAC_ADDRESS])
        connected_devices_dict = {}
        for device in connected_devices:
            connected_devices_dict[device.mac_address] = {"IP Address": device.ip_address,
                                                          "Nickname": device.nickname}
        time.sleep(60)


if __name__ == '__main__':
    process = Thread(target=loop_device_scan)
    process.start()
    socketio.run(app=app, host='0.0.0.0', debug=True, port=8000)


