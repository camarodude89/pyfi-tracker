# PyFi-Tracker

## Purpose

PyFi-Tracker gathers information about devices connected to the occupied LAN. The purpose for
gathering this information is what can be inferred from it. Such as how long devices are connected to
the network, visualizing their behavior (how often they connected/disconnected from the network), and
more importantly, inferring when people leave/arrive at home. Determining when someone has gotten home
can be done fairly easily depending on which device is being monitored. Smartphones seems to be the
best indicators of bodily presence at home. Life360 is an option for more accurate, all encompassing
indicators of when someone has left/arrived at home, but not everyone wants to or is willing to share
their GPS data at all times. So this could be used as an alternative method.

## Details

PyFi-Tracker gathers data from my CenturyLink technicolor C1100T modem through a telnet session. SSH
would have been preferred, but the modem refused to allow an SSH connection despite configuration
changes that said otherwise. A BusyBox session is then initiated, which allows access to the
device_list file. This file is updated by the modem every 4 to 5 minutes, so device connection status
is accurate to within 4 to 5 minutes. Once the file is retrieved, it is parsed into a Python
dictionary and then entered into a containerized PostgreSQL database. During the processing of the
dictionary, a notification is built to be sent through PushBullet to the specified device from the
API key provided. Connect and disconnect times are also recorded in the database for future reporting
and inferring of data.

## Planned Features

* Customization of notifications, perhaps grouping of devices by owner
* Dynamic webpage showing most recent device connection statuses (looking at Bootstrap and AJAX)