#!/bin/sh

exec xautolock -detectsleep -locker 'i3lock -i ~/.config/i3/bg/ls.png' -time 3 -notify 30 -notifier 'notify-send -u critical -t 10000 -- "LOCKING screen in 30 seconds"'
