from pushbullet import PushBullet
from auth import API_KEY


def send_pbnotification(title=None, msg=None):
    pb = PushBullet(API_KEY)
    pb.push_note(title, msg)
