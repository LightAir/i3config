#!/bin/bash
# Перечитать конфиг без перезапуска иксов
#
# XDG_CURRENT_DESKTOP=kde
# QT_QPA_PLATFORM=kde
# QT_QPA_PLATFORM_THEME=kde

xrdb ~/.Xdefaults &

#xsetroot -cursor_name left_ptr &
# обои
nitrogen --restore &

# раскладка
setxkbmap "us,ru" ",winkeys" "grp:alt_shift_toggle" &

# Локер
./locker.sh &

# Два моника
# for two monitors
# xrandr --output LVDS1 --mode 1366x768 --pos 0x0 --output VGA1 --mode 1920x1080 --pos -1920x0 &

# lxpolkit
# lxpolkit &

# плейер
# mpd &

# compton
# compton -o .2 &

# Демон уведомлений
# volnoti -T "dark"

# клипбоард
# clipit &


