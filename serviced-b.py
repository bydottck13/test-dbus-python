#!/usr/bin/env python
#from gi.repository import GLib
from gi.repository import GObject
from traceback import print_exc

import threading
import os, sys, time
import gobject
import dbus
import dbus.service

from dbus.mainloop.glib import DBusGMainLoop

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

class ServiceB(dbus.service.Object):
    def __init__(self, loop):
        self._session_bus = dbus.SessionBus()
        self._session_bus.request_name(SERVICE_NAME)
        service_name = dbus.service.BusName(SERVICE_NAME, bus=self._session_bus)
        self._loop = loop
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
        self._loop.quit()

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

def thread_signal_func(*args):
    while True:
        message = "Hello everyone at "+str(time.ctime(time.time()))+"!"
        object.HelloSignal(message)
        print "Emitting signals, using 'ctrl + c' to terminate this..."
        time.sleep(2)

def exit():
    print "Exiting the service."
    mainloop.quit()  

if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    dbus.mainloop.glib.threads_init()

    mainloop = GObject.MainLoop()
    object = ServiceB(mainloop)

    thread_emitting_signals = threading.Timer(2, thread_signal_func)
    # for using Ctrl + C to terminate this program
    thread_emitting_signals.daemon = True
    thread_emitting_signals.start()

    print("Running example service B wiht PID %d." % os.getpid())
    try:
        mainloop.run()
    except KeyboardInterrupt:
        exit()