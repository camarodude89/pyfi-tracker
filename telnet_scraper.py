import telnetlib
from auth import TELNET_USER, TELNET_PASS
import re


def start_telnet_session(gateway_ip='192.168.0.1'):
    """Returns a Telnet object ready for reading the device_list file"""
    tn = telnetlib.Telnet(gateway_ip)
    tn.read_until(b': ')
    tn.write(f'{TELNET_USER}\r\n'.encode())
    tn.read_until(b': ')
    tn.write(f'{TELNET_PASS}\r\n'.encode())

    # Starts busybox session and navigates to the data directory making ready for next command
    tn.read_until(b'\r\n >')
    tn.write(b'sh\r\n')
    tn.read_until(b'\r\n# ')
    tn.write(b'cd data\r\n')
    tn.read_until(b'\r\n# ')
    return tn


def get_devices(tn=None):
    """Returns a dictionary of the connected devices parsed from the device_list file"""
    tn = tn or start_telnet_session()
    tn.write('cat device_list\r\n'.encode())
    results = tn.read_until(b"\r\n# ")
    # tn.close()

    reg_str = "^([0-9a-f]{2}[:]){5}([0-9a-f]{2})"
    results_list = [result.strip() for result in results.decode().split('\r\n') if re.match(reg_str, result)]

    device_dict = {}

    for result in results_list:
        device_data = result.split()
        mac_address = device_data[0]
        ip_address = device_data[1]
        hostname = device_data[2]
        connected = False if device_data[7] == '0' else True
        device_dict[mac_address] = {"IP Address": ip_address, "Hostname": hostname, "Connected": connected}

    return device_dict
