#! /bin/bash
#export DBUS_SESSION_BUS_ADDRESS=$(ps ax | grep " dbus-daemon" | head -1 | awk -F'address=' '{ print $2 }')
if test -z "$DBUS_SESSION_BUS_ADDRESS"; then
	eval `cat $XDG_RUNTIME_DIR/dbus-session`
	echo "D-Bus per-session daemon address is: $DBUS_SESSION_BUS_ADDRESS"
fi
