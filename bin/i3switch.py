#!/usr/bin/env python
# i3switch.py
# -*- coding: utf-8 -*-
#
# i3 color theme switcher
#

import sys
import os
import argparse
import re
# import pprint
from shutil import copyfile
import configparser
from subprocess import call

def cb_i3(val, colors):
    '''i3 callback'''
    return ("set $" + val + " " + colors[val] + "\n")

def cb_urxvt(val, colors):
    '''urxvt callback'''
    return ("URxvt*" + val + ":" + colors[val] + "\n")

def cb_status(val, colors):
    '''i3 status callback'''
    return (val + " = \"" + colors[val] + "\"\n")

def cb_dmenu(val, colors):
    '''dmenu callback'''
    return (val + "=\"" + colors[val] + "\"\n")

def replace(old, new, reg, colors, cb):
    ''' Поиск и замена в файле по регулярному выражению  '''
    old = open(old, "r")
    new = open(new, "w")

    for line in old:
        a = re.search(reg, line.strip())
        if a and a.group(1) in colors:
            new.write(cb(a.group(1), colors))
        else:
            new.write(line)

    old.close()
    new.close()

def colorsReplace(palette, style):
    '''color replace'''
    for color in style:
        if style[color] in palette:
            style[color] = palette[style[color]]
    return style

def main(argv):
    ''' Main '''
    i3 = os.path.expanduser('~/.config/i3/')
    home = os.path.expanduser('~/')

    parser = argparse.ArgumentParser()
    parser.add_argument("theme", action='store', type=str, help='used theme')
    args = parser.parse_args()

    theme = configparser.ConfigParser()
    theme.read(['../themes/' + args.theme + '.ini'])

    palette = dict(theme.items('Palette'))
    i3Colors = colorsReplace(palette, dict(theme.items('i3Style')))
    URxvtColors = colorsReplace(palette, dict(theme.items('URxvt')))
    i3StatusColors = colorsReplace(palette, dict(theme.items('i3Status')))
    dmenuColors = colorsReplace(palette, dict(theme.items('Dmenu')))

    sets = re.compile(r'.*set.*\$(.*)\s+(\S+)')
    replace("../configs/config", "/tmp/i3config", sets, dict(home=i3), cb_i3)
    replace("/tmp/i3config", i3 + "config", sets, i3Colors, cb_i3)

    urxvt = re.compile(r'.*URxvt\*(.*):\s*(\S+)')
    replace("../configs/.Xdefaults", home + ".Xdefaults", urxvt, URxvtColors, cb_urxvt)

    i3status= re.compile(r'\s*(.*)\s+(=|\+=)\s+"(.*)"')
    replace("../configs/i3status", i3 + "i3status", i3status, i3StatusColors, cb_status)

    dmenu = re.compile(r'\s*(.*)\s*=\s*"(.*)"')
    replace("../configs/dmenu.sh", i3 + "bin/dmenu.sh", dmenu, dmenuColors, cb_dmenu)

    call(["i3-msg", "restart"])
    call(["xrdb", home + ".Xdefaults"])
    call(["chmod", "+x", i3 + "bin/dmenu.sh"])

    print('ok')

if __name__ == "__main__":
    main(sys.argv[1:])
