from pushbullet import PushBullet
from auth import API_KEY


class PBNotification:

    def __init__(self, title='PyFi Alert', msg=''):
        self.pb = PushBullet(API_KEY)
        self.connected_list = []
        self.disconnected_list = []
        self.title = title
        self.msg = msg

    def add_connected_device(self, device):
        self.connected_list.append(device)

    def add_disconnected_device(self, device):
        self.disconnected_list.append(device)

    def construct_msg(self):
        con_device_list_len = len(self.connected_list)
        if con_device_list_len == 1:
            self.msg += f'{self.connected_list[0]} is connected.'
        elif con_device_list_len == 2:
            self.msg += f'{self.connected_list[0]} and {self.connected_list[1]} are connected.'
        elif con_device_list_len >= 3:
            self.msg += f'{", ".join(self.connected_list[:-1])}, and {self.connected_list[-1]} are connected.'

        if self.msg != '':
            self.msg += ' '

        discon_device_list_len = len(self.disconnected_list)
        if discon_device_list_len == 1:
            self.msg += f'{self.disconnected_list[0]} is disconnected.'
        elif discon_device_list_len == 2:
            self.msg += f'{self.disconnected_list[0]} and {self.disconnected_list[1]} are disconnected.'
        elif discon_device_list_len >= 3:
            self.msg += f'{", ".join(self.disconnected_list[:-1])}, and {self.disconnected_list[-1]} are disconnected.'

    def send_notification(self):
        self.construct_msg()
        if self.msg != '':
            self.pb.push_note(self.title, self.msg)
