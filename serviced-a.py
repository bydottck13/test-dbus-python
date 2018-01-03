#!/usr/bin/env python
from gi.repository import GLib
from traceback import print_exc

import os, sys
import dbus
import dbus.service

from dbus.mainloop.glib import DBusGMainLoop

SERVICE_NAME = "com.cybernut.demoA"
INTERFACE_NAME = "com.cybernut.demoA"
OBJECT_PATH = "/ServiceA"

"""
types for signature: 
BYTE: y
BOOLEAN: b
INT16: n, UINT16: q
INT32: i, UINT32: u
INT64: x, UINT64: t
DOUBLE: d
OBJECT_PATH: o
SIGNATURE: g
STRING: s
TUPLES: a{xy}, x: key, y: value, e.g. a{s(ii)}: keys are string, and values are two INT32
ARRAY: a, ARRAY of two Int32: a(ii)
"""

def hello_signals_handler(hello_string):
    print "Received a hello signal and it says '" + hello_string+"'"

class ServiceA(dbus.service.Object):
    def __init__(self, loop):
        self._session_bus = dbus.SessionBus()
        self._session_bus.request_name(SERVICE_NAME)
        self._service_name = dbus.service.BusName(SERVICE_NAME, bus=self._session_bus)
        self._loop = loop
        dbus.service.Object.__init__(self, self._service_name, OBJECT_PATH)

        # signals
        self._session_bus.add_signal_receiver(hello_signals_handler, 
            dbus_interface="com.cybernut.demoB", signal_name="HelloSignal")

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='xx', out_signature='x')
    def Multiply(self, x, y):
        return int(x * y)

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='s')
    def Hello(self, hello_message):
        print (str(hello_message))
        return str("Hello test!")

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='')
    def HelloNoReply(self, hello_message):
        print (str(hello_message))

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='', out_signature='')
    def Exit(self):
        self._loop.quit()

def exit():
    print "Exiting the service."
    mainloop.quit()   

if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)

    mainloop = GLib.MainLoop()
    object = ServiceA(mainloop)
    
    print("Running example service A wiht PID %d." % os.getpid())
    try:
        mainloop.run()
    except KeyboardInterrupt:
        exit()