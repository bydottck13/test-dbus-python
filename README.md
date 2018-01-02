# ***** NOTICE *****
This is a dbus example by using python-dbus includes testing to emit signals and to call methods with D-BUS architecture.

------

## DESCRIPTIONS
For using traditional services which are based on dbus and C code on ROS platform, a OS that is rely on C++/Phtyon, this example provides a bridge between dbus and ROS.

## REQUIREMENTS
Testing OS: ubuntu-16.04.2-desktop-amd64
* Install python-dbus
```
$ sudo apt-get install python-dbus
```

## USAGES
```
$ python serviced-a.py
```
Open a new terminal
```
$ python serviced-b.py
```

## MISCELLANEOUS
Some useful tools for debugging:
* `D-Feet` - install from Ubuntu Software
* `busctl` - e.g. busctl --user tree INTERFACE_NAME
* `dbus-monitor` - execute from CL

## REFERENCE
* [dbus-python 1.2.4](https://pypi.python.org/pypi/dbus-python)
