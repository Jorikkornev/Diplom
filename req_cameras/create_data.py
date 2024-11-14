# TODO Создать функцию get_data(Dict | json | False) -> Dict,
#  которая обрабатывает данные, полученные от ф-ии get_cameras_status()
# TODO В случае, если get_cameras_status() возвращает False - передаёт сообщение об ошибке тг боту
# TODO запускать с помощью schedule get_cameras_status() с интервалом каждый час
# TODO Создать функцию set_data(Dict | json) -> Dict для записи обработанных данных SQLlite БД, отправку боту
# TODO добавить тестирование
# TODO V 1.1 - переписать в класс, добавить Pydatic, SqlAlchemy, модели данных и валидацию

import schedule

schedule.every().hour.do()