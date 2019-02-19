from entities import Device, DeviceOwner, DeviceConnectionLog,\
    Base, Session, engine


class DatabaseActions:

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def process_device_dict(self):
        pass

    def populate_databases(self, devices_dict):
        for k, v in devices_dict.items():
            mac_address = k
            ip_address = v['IP Address']
            hostname = v['Hostname']
            connected = v['Connected']
            device = Device(mac_address=mac_address, ip_address=ip_address,
                            hostname=hostname, connected=connected)
            self.session.add(device)
        self.session.commit()
        self.session.close()
