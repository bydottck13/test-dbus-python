#! /bin/bash
export DBUS_SESSION_BUS_ADDRESS=$(ps ax | grep " dbus-daemon" | head -1 | awk -F'address=' '{ print $2 }')
