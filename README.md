# i3config
The configuration includes i3 theme switcher.

Конфигураци включает в себя i3 theme switcher.

## Зависимости
## Depends

[i3-gaps](https://aur.archlinux.org/packages/i3-gaps-git/)

[dmenu](https://www.archlinux.org/packages/?name=dmenu)

[Font Roboto Condensed](https://aur.archlinux.org/packages/ttf-roboto/)

[Font Awesome](https://aur.archlinux.org/packages/ttf-font-awesome/)

[DvorakRus](https://github.com/LightAir/DvorakRus)

[tvolnoti](https://github.com/LightAir/tvolnoti)

nitrogen, mpd, compton, lxpolkit, xrandr, xbacklight, rxvt

## Install
Copy the entire contents of the directory in ~/.config/i3

Set path for config dir in i3config/configs/config file (line 62)

Go to the folder ~/.config/i3/bin

Run ```python i3switch.py theme_name```, where theme_name theme from "themes" folder

Customize according to your preferences autostart.sh

Customize settings your app in i3config/bin/apprun/ directory

## Установка
Скопировать всё содержимое этой директории в ~/.config/i3

Установите путь к директории с конфигурационнным файлом в файле i3config/configs/config (строка 62)

Перейти в папку ~/.config/i3/bin

Запустить ```python i3switch.py theme_name```, где theme_name тема из папки themes

Настройте в зависимости от ваших предпочтений autostart.sh

Настройте параметры своих программ в директории i3config/bin/apprun/

## Горячие клавишы
[hotkeys](hotkeys.md)

# Themes
## dark

![scrrenshot](/screenshots/dark-desktop.png)

![scrrenshot](/screenshots/dark-urxvt.png)

![scrrenshot](/screenshots/dark-workspace.png)

## white-red

![scrrenshot](/screenshots/wr-desktop.png)

![scrrenshot](/screenshots/wr-urxvt.png)

![scrrenshot](/screenshots/wr-workspace.png)

## gray
![scrrenshot](/screenshots/gray-desktop.png)

![scrrenshot](/screenshots/gray-urxvt.png)

![scrrenshot](/screenshots/gray-workspace.png)
