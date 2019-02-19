from flask import Flask, render_template
from threading import Thread
import time
import telnet_scraper
from actions import DatabaseActions

app = Flask(__name__)


@app.route('/')
def show_table():
    return render_template('index.html', device_dict=device_dict)


def loop_device_scan():
    telnet_session = telnet_scraper.start_telnet_session()
    while True:
        global device_dict
        device_dict = telnet_scraper.get_devices(telnet_session)
        db_actions = DatabaseActions()
        db_actions.populate_databases(device_dict)
        time.sleep(60)


if __name__ == '__main__':
    process = Thread(target=loop_device_scan)
    process.start()
    app.run(host='0.0.0.0', debug=True, port=8000)


