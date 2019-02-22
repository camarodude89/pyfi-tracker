from entities import Device, DeviceOwner, DeviceConnectionLog,\
    Base, Session, engine
from sqlalchemy import exists
from datetime import datetime
from notifications import send_pbnotification


class DatabaseActions:

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def process_device_dict(self, devices_dict):
        current_time = datetime.now()
        for k, v in devices_dict.items():
            # checks to see if any new devices have connected, if so add them
            device_exists = self.session.query(exists().where(Device.mac_address == k)).scalar()
            if not device_exists:
                mac_address = k
                ip_address = v['IP Address']
                hostname = v['Hostname']
                connected = v['Connected']
                device = Device(mac_address=mac_address, ip_address=ip_address,
                                hostname=hostname, connected=connected)
                self.session.add(device)

            # update connection states for devices
            db_device = self.session.query(Device).filter(Device.mac_address == k).scalar()
            prev_con_status = db_device.connected
            cur_con_status = v['Connected']
            if prev_con_status != cur_con_status:
                db_device.connected = cur_con_status

                # update the device_connection_log for the device
                if db_device.connected:
                    con_log_entry = DeviceConnectionLog(mac_address=db_device.mac_address,
                                                        connected=current_time)
                    self.session.add(con_log_entry)
                    msg = f'{db_device.hostname if db_device.nickname is None else db_device.nickname} connected.'
                    send_pbnotification(title='PyFi Alert', msg=msg)
                else:
                    con_log_entry = self.session.query(DeviceConnectionLog).filter(
                        DeviceConnectionLog.mac_address == k, DeviceConnectionLog.disconnected is None).scalar()
                    con_log_entry.disconnected = current_time
                    msg = f'{db_device.hostname if db_device.nickname is None else db_device.nickname} disconnected.'
                    send_pbnotification(title='PyFi Alert', msg=msg)

        self.session.commit()

    def populate_device_db(self, devices_dict):
        for k, v in devices_dict.items():
            mac_address = k
            ip_address = v['IP Address']
            hostname = v['Hostname']
            device = Device(mac_address=mac_address, ip_address=ip_address,
                            hostname=hostname, connected=False)
            self.session.add(device)
        self.session.commit()
        self.session.close()

    def query_connected_devices(self):
        return self.session.query(Device).filter(Device.connected.is_(True)).all()
