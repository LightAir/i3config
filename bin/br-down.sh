#!/bin/bash

xbacklight -5

BR=`xbacklight -get | sed -r 's/\..+//'`

eval "volnoti-show -s /usr/share/pixmaps/volnoti/display-brightness-dark.svg $BR"
