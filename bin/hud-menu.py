#!/usr/bin/env python3

import dbus
import subprocess
import sys
import logging
import time

def format_label_list(label_list):
    head, *tail = label_list
    result = head
    for label in tail:
        result = result + " > " + label
    result = result.replace("Root > ", "")
    result = result.replace("_", "")
    return result


def try_app_menu_interface(window_id):
    # --- Get Appmenu Registrar DBus interface
    session_bus = dbus.SessionBus()
    try:
        appmenu_registrar_object = session_bus.get_object('com.canonical.AppMenu.Registrar',
                                                          '/com/canonical/AppMenu/Registrar')
        appmenu_registrar_object_iface = dbus.Interface(appmenu_registrar_object, 'com.canonical.AppMenu.Registrar')
    except dbus.exceptions.DBusException:
        logging.info('Unable to register with com.canonical.AppMenu.Registrar.')
        return

    # --- Get dbusmenu object path
    try:
        dbusmenu_bus, dbusmenu_object_path = appmenu_registrar_object_iface.GetMenuForWindow(window_id)
    except dbus.exceptions.DBusException:
        logging.info('Unable to get dbusmenu object path.')
        return

    # --- Access dbusmenu items
    # --- Access dbusmenu items
    try:
        dbusmenu_object = session_bus.get_object(dbusmenu_bus, dbusmenu_object_path)
        dbusmenu_object_iface = dbus.Interface(dbusmenu_object, 'com.canonical.dbusmenu')
    except ValueError:
        logging.info('Unable to access dbusmenu items.')
        return

    #dbusmenu_items = dbusmenu_object_iface.GetLayout(0, -1, ["label"])
    dbusmenu_items = dbusmenu_object_iface.GetLayout(0, 0, ["label", "children-display"])

    dbusmenu_item_dict = dict()

    # For excluding items which have no action
    blacklist = []

    """ explore_dbusmenu_item """

    def explore_dbusmenu_item(item, label_list):
        item_id = item[0]
        item_props = item[1]

        # expand if necessary
        if 'children-display' in item_props:
            dbusmenu_object_iface.AboutToShow(item_id)
            dbusmenu_object_iface.Event(item_id, "opened", "not used", dbus.UInt32(time.time())) #fix firefox
        try:
            item = dbusmenu_object_iface.GetLayout(item_id, 1, ["label", "children-display"])[1]
        except:
            return

        item_children = item[2]

        if 'label' in item_props:
            new_label_list = label_list + [item_props['label']]
        else:
            new_label_list = label_list

        if len(item_children) == 0:
            if new_label_list not in blacklist:
                dbusmenu_item_dict[format_label_list(new_label_list)] = item_id
        else:
            blacklist.append(new_label_list)
            for child in item_children:
                explore_dbusmenu_item(child, new_label_list)

    explore_dbusmenu_item(dbusmenu_items[1], [])

    menu_keys = sorted(dbusmenu_item_dict.keys())

    # --- Run rofi/dmenu
    head, *tail = menu_keys
    menu_string = head
    for m in tail:
        menu_string += '\n'
        menu_string += m

    if 'dmenu' in sys.argv:
        menu_cmd = subprocess.Popen(['dmenu', '-i', '-l', '12'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    else:
        menu_cmd = subprocess.Popen(
            ['rofi', '-dmenu', '-i', '-location', '1', '-width', '100', '-l', '12', '-scroll-method', '1',
             '-color-enabled', '-color-window', "#21252E, #ffffff", '-color-normal',
             "#242424, #FFFFFF, #242424, #769070", '-separator-style', 'solid', '-p', '', '-font',
             "Roboto Condensed 10", '-show', 'combi', '-show-icons'], stdout=subprocess.PIPE,
            stdin=subprocess.PIPE)
    menu_cmd.stdin.write(menu_string.encode('utf-8'))
    menu_result = menu_cmd.communicate()[0].decode('utf8').rstrip()
    menu_cmd.stdin.close()

    if menu_result.endswith("\n"):
        menu_result = menu_result[:-1]

    # --- Use menu result
    if menu_result in dbusmenu_item_dict:
        action = dbusmenu_item_dict[menu_result]
        dbusmenu_object_iface.Event(action, 'clicked', 0, 0)


def try_gtk_interface(gtk_bus_name_cmd, gtk_object_path_cmd):
    gtk_bus_name = gtk_bus_name_cmd.split(' ')[2].split('\n')[0].split('"')[1]
    # print(gtk_object_path_cmd)
    gtk_object_path = gtk_object_path_cmd.split(' ')[2].split('\n')[0].split('"')[1]
    # print("GTK MenuModel Bus name and object path: ", gtk_bus_name, gtk_object_path)

    # --- Ask for menus over DBus ---
    session_bus = dbus.SessionBus()
    gtk_menubar_object = session_bus.get_object(gtk_bus_name, gtk_object_path)
    gtk_menubar_object_iface = dbus.Interface(gtk_menubar_object, dbus_interface='org.gtk.Menus')
    gtk_action_object_actions_iface = dbus.Interface(gtk_menubar_object, dbus_interface='org.gtk.Actions')
    gtk_menubar_results = gtk_menubar_object_iface.Start([x for x in range(1024)])

    # --- Construct menu list ---
    gtk_menubar_menus = dict()
    for gtk_menubar_result in gtk_menubar_results:
        gtk_menubar_menus[(gtk_menubar_result[0], gtk_menubar_result[1])] = gtk_menubar_result[2]

    gtk_menubar_action_dict = dict()
    # gtk_menubar_target_dict = dict()

    """ explore_menu """

    def explore_menu(menu_id, label_list):
        if menu_id in gtk_menubar_menus:
            for menu in gtk_menubar_menus[menu_id]:
                if 'label' in menu:
                    menu_label = menu['label']
                    new_label_list = label_list + [menu_label]
                    formatted_label = format_label_list(new_label_list)

                    if 'action' in menu:
                        menu_action = menu['action']
                        if ':section' not in menu and ':submenu' not in menu:
                            gtk_menubar_action_dict[formatted_label] = menu_action
                        # if 'target' in menu:
                        # menu_target = menu['target']
                        # gtk_menubar_target_dict[formatted_label] = menu_target

                if ':section' in menu:
                    menu_section = menu[':section']
                    section_menu_id = (menu_section[0], menu_section[1])
                    explore_menu(section_menu_id, label_list)

                if ':submenu' in menu:
                    menu_submenu = menu[':submenu']
                    submenu_menu_id = (menu_submenu[0], menu_submenu[1])
                    explore_menu(submenu_menu_id, new_label_list)

    explore_menu((0, 0), [])

    menu_keys = sorted(gtk_menubar_action_dict.keys())

    # --- Run rofi/dmenu
    head, *tail = menu_keys
    menu_string = head
    for m in tail:
        menu_string += '\n'
        menu_string += m

    if 'dmenu' in sys.argv:
        menu_cmd = subprocess.Popen(['dmenu', '-i', '-l', '15'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    else:
        menu_cmd = subprocess.Popen(
            ['rofi', '-dmenu', '-i', '-location', '1', '-width', '100', '-l', '15', '-scroll-method', '1',
             '-color-enabled', '-color-window', "#242424, #ffffff", '-color-normal',
             "#242424, #FFFFFF, #242424, #398ee7", '-separator-style', 'solid', '-p', ''], stdout=subprocess.PIPE,
            stdin=subprocess.PIPE)
    menu_cmd.stdin.write(menu_string.encode('utf-8'))
    menu_result = menu_cmd.communicate()[0].decode('utf8').rstrip()
    menu_cmd.stdin.close()

    if menu_result.endswith("\n"):
        menu_result = menu_result[:-1]

    # --- Use menu result
    if menu_result in gtk_menubar_action_dict:
        action = gtk_menubar_action_dict[menu_result]
        # print('GTK Action :', action)
        gtk_action_object_actions_iface.Activate(action.replace('unity.', ''), [], dict())


"""
  main
"""

# --- Get X Window ID ---
window_id_cmd = subprocess.check_output(['xprop', '-root', '-notype', '_NET_ACTIVE_WINDOW']).decode('utf-8')
glob_window_id = window_id_cmd.split(' ')[4].split(',')[0].split('\n')[0]

# For testing get the id of the target window from xwininfo
# window_id = '0x3400186'
# print('Window id is :', window_id)

# --- Get GTK MenuModel Bus name ---
global_gtk_bus_name_cmd = \
    subprocess.check_output(['xprop', '-id', glob_window_id, '-notype', '_GTK_UNIQUE_BUS_NAME']).decode('utf-8')
global_gtk_object_path_cmd = \
    subprocess.check_output(['xprop', '-id', glob_window_id, '-notype', '_GTK_MENUBAR_OBJECT_PATH']).decode('utf-8')

print(global_gtk_bus_name_cmd)
print(global_gtk_object_path_cmd)

if (global_gtk_bus_name_cmd == '_GTK_UNIQUE_BUS_NAME:  not found.\n' or
        global_gtk_bus_name_cmd == '_GTK_UNIQUE_BUS_NAME:  no such atom on any window.\n' or
        global_gtk_object_path_cmd == '_GTK_MENUBAR_OBJECT_PATH:  no such atom on any window.\n' or
        global_gtk_object_path_cmd == '_GTK_MENUBAR_OBJECT_PATH:  not found.\n'):
    try_app_menu_interface(int(glob_window_id, 16))
else:
    try_gtk_interface(global_gtk_bus_name_cmd, global_gtk_object_path_cmd)
