#!/usr/bin/env python
from gi.repository import GLib

import sys
from traceback import print_exc

import threading
import time

import dbus
import dbus.service

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

SERVICE_NAME = "com.cybernut.demoB"
INTERFACE_NAME = "com.cybernut.demoB"
OBJECT_PATH = "/ServiceB"

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

class dbusThread(threading.Thread):
    def __init__(self, mainLoop):
        threading.Thread.__init__(self)
        self._loop = mainLoop

    def run(self):
        self._loop.run()

class ServiceB(dbus.service.Object):
    def __init__(self):
        self._session_bus = dbus.SessionBus()
        self._session_bus.request_name(SERVICE_NAME)
        service_name = dbus.service.BusName(SERVICE_NAME, bus=self._session_bus)
        dbus.service.Object.__init__(self, service_name, OBJECT_PATH)

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='xx', out_signature='x')
    def DoMultiply(self, x, y):
        try:
            remote_object = self._session_bus.get_object("com.cybernut.demoA",
                    "/ServiceA")
            multiply_reply = remote_object.Multiply(x, y,
                dbus_interface = "com.cybernut.demoA")
        except dbus.DBusException:
            print_exc()
            sys.exit(1)

        print ("The result is "+str(multiply_reply))
        return multiply_reply

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='', out_signature='')
    def Exit(self):
        mainloop.quit()

    @dbus.service.signal(dbus_interface=INTERFACE_NAME)
    def HelloSignal(self, message):
        # The signal is emitted when this method exits
        # You can have code here if you wish
        pass

    @dbus.service.method(dbus_interface=INTERFACE_NAME)
    def emitHelloSignal(self):
        #you emit signals by calling the signal's skeleton method
        self.HelloSignal('Hello')
        return 'Signal emitted'

if __name__ == "__main__":
    object = ServiceB()
    loop = GLib.MainLoop()
    print "Running example service B."

    dbusThread = dbusThread(loop)

    print "Emitting signals, using 'ctrl + z' to terminate this..."
    while 1:
        message = "Good at "+str(time.ctime(time.time()))
        object.HelloSignal(message)
        print "Emitting signals, using 'ctrl + z' to terminate this..."
        time.sleep(2)
        pass
