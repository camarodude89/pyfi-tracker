from flask import Flask, render_template
from threading import Thread
import time
import telnet_scraper
from actions import DatabaseActions

app = Flask(__name__)
db_actions = DatabaseActions()

@app.route('/')
def show_table():
    return render_template('index.html',
                           connected_devices=db_actions.query_connected_devices())


def loop_device_scan():
    telnet_session = telnet_scraper.start_telnet_session()
    while True:
        device_dict = telnet_scraper.get_devices(telnet_session)
        db_actions.process_device_dict(device_dict)
        time.sleep(60)


if __name__ == '__main__':
    process = Thread(target=loop_device_scan)
    process.start()
    app.run(host='0.0.0.0', debug=True, port=8000)


