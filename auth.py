import keyring

API_KEY = keyring.get_password('pushbullet', 'api_key')
PSQL_USER = keyring.get_password('postgres', 'username')
PSQL_PASS = keyring.get_password('postgres', PSQL_USER)
TELNET_USER = keyring.get_password('CenturyLink', 'username')
TELNET_PASS = keyring.get_password("CenturyLink", TELNET_USER)
