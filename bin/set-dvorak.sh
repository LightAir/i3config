#!/bin/bash

setxkbmap "dvorak,ru" ",rud" "grp:alt_shift_toggle"

notify-send --expire-time=50 "Dvorak keyboard"
