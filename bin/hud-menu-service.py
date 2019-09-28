#!/usr/bin/env python3

from gi.repository import Gtk
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop


class HudMenuService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName('com.canonical.AppMenu.Registrar', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/com/canonical/AppMenu/Registrar')
        self.window_dict = dict()

    @dbus.service.method('com.canonical.AppMenu.Registrar', in_signature='uo', sender_keyword='sender')
    def RegisterWindow(self, window_id, menu_object_path, sender):
        self.window_dict[window_id] = (sender, menu_object_path)

    @dbus.service.method('com.canonical.AppMenu.Registrar', in_signature='u', out_signature='so')
    def GetMenuForWindow(self, window_id):
        if window_id in self.window_dict:
            sender, menu_object_path = self.window_dict[window_id]
            return [dbus.String(sender), dbus.ObjectPath(menu_object_path)]

    @dbus.service.method('com.canonical.AppMenu.Registrar')
    def Q(self):
        Gtk.main_quit()


DBusGMainLoop(set_as_default=True)
HudMenuService()
Gtk.main()

# GTK apps : get dbus service (xprop)
