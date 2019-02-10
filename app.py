from flask import Flask, render_template
import telnetlib
import keyring

app = Flask(__name__)


@app.route('/')
def hello_world():
    device_dict = connected_devices()
    return render_template('index.html', device_dict=device_dict)


def connected_devices():
    tn = telnetlib.Telnet('192.168.0.1')
    tn.read_until(b": ").decode()
    username = keyring.get_password('CenturyLink', 'username')
    tn.write(f'{username}\r\n'.encode())
    tn.read_until(b": ").decode()
    tn.write(f'{keyring.get_password("CenturyLink", username)}\r\n'.encode())
    tn.read_until(b"\r\n >").decode()
    tn.write('lanhosts show all\r\n'.encode())
    results = tn.read_until(b"\r\n >")
    tn.close()

    import re
    reg_str = "^([0-9a-f]{2}[:]){5}([0-9a-f]{2})"
    results_list = [str.strip() for str in results.decode().split('\r\n') if re.match(reg_str, str)]

    device_dict = {}

    for result in results_list:
        device_data = result.split()
        mac_address = device_data[0]
        ip_address = device_data[1]
        hostname = device_data[3]
        device_dict[mac_address] = {"IP Address": ip_address, "Hostname": hostname}

    return device_dict


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
