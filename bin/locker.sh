#!/bin/sh

xautolock -detectsleep -locker 'i3lock -i ~/.config/i3/bg/ls.png' -time 10 -notify 30 -notifier 'notify-send -u critical -t 10000 -- "LOCKING screen in 30 seconds"'
