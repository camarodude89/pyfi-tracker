from pushbullet import PushBullet

API_KEY = 'o.bG1R7FW8RuNdTysbAepbBzuKfQ9xhlVT'

def send_pbnotification(title=None, msg=None):
    pb = PushBullet(API_KEY)
    pb.push_note(title, msg)