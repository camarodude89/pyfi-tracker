from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Boolean, ARRAY, DateTime, Integer
import keyring


psql_user = keyring.get_password('postgres', 'username')
psql_pass = keyring.get_password('postgres', psql_user)

engine = create_engine(f'postgresql://{psql_user}:{psql_pass}@localhost:5432/pyfi')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Device(Base):
    __tablename__ = 'device'

    mac_address = Column(String, primary_key=True)
    ip_address = Column(String)
    hostname = Column(String)
    nickname = Column(String)
    connected = Column(Boolean)
    watched = Column(Boolean)

    def __init__(self, mac_address=None, ip_address=None, hostname=None, nickname=None,
                 connected=False, watched=False):
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.hostname = hostname
        self.nickname = nickname
        self.connected = connected
        self.watched = watched


class DeviceConnectionLog(Base):
    __tablename__ = 'device_connection_log'

    id = Column(Integer, primary_key=True)
    mac_address = Column(String)
    connected = Column(DateTime)
    disconnected = Column(DateTime)

    def __init__(self, mac_address=None, connected=None, disconnected=None):
        self.mac_address = mac_address
        self.connected = connected
        self.disconnected = disconnected


class DeviceOwner(Base):
    __tablename__ = 'device_owner'

    mac_address = Column(String, primary_key=True)
    owner = Column(String)

    def __index__(self, mac_address, owner):
        self.mac_address = mac_address
        self.owner = owner

