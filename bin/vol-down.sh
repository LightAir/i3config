#!/bin/bash

VOL=`amixer -D pulse sset Master 5%- | cut -d"[" -f2 | sed -r 's/%.+//' | awk 'NR == 6{print}'`

if [ "$VOL" = "0" ]
then
	eval "volnoti-show -m $VOL"
else
	eval "volnoti-show $VOL"
fi
