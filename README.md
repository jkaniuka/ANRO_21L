Nowy plik

**Wrzuciłem pierwszą wersję programu do sterowania żółwiem**
- pakiet  nazywa się turtle_keyboard
- sterowanie odbywa się poprzez bibliotekę konsolową

Uruchamianie:

W pierwszej konsoli:

. install/setup.bash

ros2 run turtle_keyboard param_talker

W drugiej konsoli trzeba otworzyć turtlesim, domyślnie steruje się w,a,s,d

Progam działa, ale jest problem przy próbie wczytania parametrów:

Otwieram nową konsolę i wpisuję:     . install/setup.bash i potem ros2 param list

Wyskakuje błąd: Exception while calling service of node '/my_publisher_node': None

Nie wiem czemu tak się dzieje :( ; polecenie ros2 node list wykrywa normalnie węzeł.
Jak problem z tym błędem się rozwiąże to zostaje jeszcze dorobienie pliku .roslauch



