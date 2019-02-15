from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Boolean, ARRAY, TIMESTAMP

engine = create_engine('postgresql://pyfiuser:pyfipsql@localhost:5432/pyfi')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Devices(Base):
    __tablename__ = 'devices'

    mac_address = Column(String, primary_key=True)
    ip_address = Column(String)
    hostname = Column(String)
    nickname = Column(String)
    connected = Column(Boolean)
    watched = Column(Boolean)

    def __init__(self, mac_address, ip_address, hostname, nickname,
                 connected=False, watched=False):
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.hostname = hostname
        self.nickname = nickname
        self.connected = connected
        self.watched = watched


class DeviceConnectionLog(Base):
    __tablename__ = 'device_connection_log'

    mac_address = Column(String)
    connected_timeframe = Column(ARRAY(TIMESTAMP))

    def __init__(self, mac_address, connected_timeframe):
        self.mac_address = mac_address
        self.connected_timeframe = connected_timeframe


class DeviceOwner(Base):
    __tablename__ = 'device_owner'

    mac_address = Column(String, primary_key=True)
    owner = Column(String)

    def __index__(self, mac_address, owner):
        self.mac_address = mac_address
        self.owner

