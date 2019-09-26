# i3config v3

Конфигураци включает в себя i3 theme switcher.

## Зависимости

### Обязательные
Что бы расстояния между окнами были [i3-gaps](https://aur.archlinux.org/packages/i3-gaps-git/)

Улучшеное dmenu [dmenu2](https://aur.archlinux.org/packages/dmenu2/)

Иконки [Font Awesome](https://aur.archlinux.org/packages/ttf-font-awesome/)

Используемый шрифт [Font Roboto Condensed](https://aur.archlinux.org/packages/ttf-roboto/)

Установка обоев [Nitrogen](https://www.archlinux.org/packages/extra/x86_64/nitrogen/)

Мега гибкий терминал [rxvt-unicode](https://wiki.archlinux.org/index.php/Rxvt-unicode_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9))

xrandr - программа настройки оконной системы X

xbacklight - управление яркостью экрана,

scrot - создание скриншотов экрана

В ubuntu скорее всего придётся дополнительно поставить python-configparser

Установит gaps можно по вот [так](https://github.com/pasiegel/i3-gaps-install-ubuntu)

### Что ещё можно поставить

Русская раскладка дворака [DvorakRus](https://github.com/LightAir/DvorakRus)

Нотификация [tvolnoti](https://github.com/LightAir/tvolnoti)

mpd - плейер 

compton - композитный менеджер

lxpolkit - средство для управления правами приложений пользовательского уровня (lxsession)

rofi - красивая замена dmenu 'sudo pacman -S rofi'

## Установка
Установить зависимости.

```
yaourt -S dmenu2 luastatus-git
```

```
sudo pacman -S i3-gaps i3lock i3blocks ttf-roboto ttf-font-awesome rxvt-unicode xorg-xrandr xorg-xbacklight nitrogen scrot
```

Если нужны дополнительные зависимости (tvolnoti и DvorakRus ставятся руками)
```
sudo pacman -S mpd lxsession compton
```

Скопировать всё содержимое этой директории в ~/.config/i3

Перейти в папку ~/.config/i3/bin

Запустить ```python i3switch.py theme_name```, где theme_name тема из папки themes

Настройте в зависимости от ваших предпочтений autostart.sh

Настройте параметры своих программ в директории i3config/bin/apprun/

## Горячие клавиши
[Горячие клавиши](hotkeys.ru.md)

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
