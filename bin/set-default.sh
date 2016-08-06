#!/bin/bash

setxkbmap "us,ru" ",winkeys" "grp:alt_shift_toggle"

notify-send --expire-time=50 "Standart keyboard"
