# TODO Создать функцию get_data(Dict | json | False) -> Dict,
#  которая обрабатывает данные, полученные от ф-ии get_cameras_status()
# TODO В случае, если get_cameras_status() возвращает False - передаёт сообщение об ошибке тг боту
# TODO запускать с помощью schedule get_cameras_status() с интервалом каждый час
# TODO Создать функцию set_data(Dict | json) -> Dict для записи обработанных данных SQLlite БД, отправку боту
# TODO добавить тестирование
# TODO V 1.1 - переписать в класс, добавить Pydatic, SqlAlchemy, модели данных и валидацию
import logging
import threading
import time
from typing import List

import schedule
from schedule import every, repeat,run_pending
from req_cameras.parser_selenium import get_cams, logger

logging.basicConfig()
schedule_logger = logging.getLogger('schedule')
schedule_logger.setLevel(level=logging.DEBUG)

test = ["AE2511420\nAE2511420\n31.173.83.105\nOffline",
        "AE2512537\nAE2512537\n178.176.76.181\nOffline",
        "AG7265526\nAG7265526\n31.173.87.38\nOnline",
        "AF8486640\nAF8486640\n31.173.80.206\nOnline"
        ]

# Data model
# "online_status" - данные с сайта - 1 - Online, 0 - Offline
# "status" - статус учёта камеры - 1 - на мониторинге, 0 - не на мониторинге
cam = ["domain", "serial", "ip", "online_status", "time_stamp"]

# cameras - тестовые данные, имитирующие выборку из таблицы monitoring_cams, нужны для сравнения с данными,
# полученными в результате запроса к сайту - cam_data. Условия сравнения и значения -
# serial == serial and status !=0 and online_status == 1, камеры на мониторинге, но не онлайн заносятся в offline_cams
# и отправляются ТГ боту, в БД offline_cams
cameras = [{'domain': 'AE2511420', 'serial': 'AE2511420', 'ip': '31.173.83.105', 'online_status': 0, 'status': 0,
            'time_stamp': '1732134604'},
           {'domain': 'AE2512537', 'serial': 'AE2512537', 'ip': '178.176.76.181', 'online_status': 1, 'status': 1,
            'time_stamp': '1732134075'},
           {'domain': 'AG7265526', 'serial': 'AG7265526', 'ip': '31.173.87.38', 'online_status': 1, 'status': 1,
            'time_stamp': '1732134075'},
           {'domain': 'AF8486640', 'serial': 'AF8486640', 'ip': '178.176.72.189', 'online_status': 1, 'status': 1,
            'time_stamp': '1732134075'}
           ]
# Для получения значения из schedule
cam_data = []

# Для получения данных по офлайн камерам
offline_cams = []


# Парсинг полученных данных
def parsing_data(cams_list: List, field_names: List) -> List:
    global cam_data
    if cam_data:
        cam_data = []
    # Добавление временной метки, изменение online_status с текста на число или bool
    pars_cams_list = [cam_list + f"\n{time.time()}" for cam_list in cams_list]
    pars_cams_list = [cam_list.split('\n') for cam_list in pars_cams_list]
    for cam_list in pars_cams_list:
        for i in range(len(cam_list)):
            if cam_list[i] == 'Online':
                cam_list[i] = 1
            elif cam_list[i] == 'Offline':
                cam_list[i] = 0
    for cam_item in pars_cams_list:
        cam_data.append(dict(zip(field_names, cam_item)))
    #logger.info("schedule RUN from: parsing_data")
    print("cam_data", cam_data)
    return cam_data


# Сравнение базовых данных с полученными с сайта
def change_data(base_data: List, new_data: List) -> List:
    global offline_cams
    for b in base_data:
        for n in new_data:
            if b['serial'] == n['serial'] and b["status"] != 0 and n["online_status"] == 0:
                offline_cams.append(b)
    return offline_cams


# Отправка данных в тг бот, БД



# Start all functions
def run_all():
    global cam_data, offline_cams, cam, cameras
    cam_data = parsing_data(cam_data, cam)
    offline_cams = change_data(cameras, cam_data)
    print('cam_data: \n', cam_data, '\n offline_cams: ', offline_cams)
    cam_data = []


# Для запуска ф-ии schedule get_cams
@repeat(schedule.every(3).minutes)
def run_get_cams_timer():  # (func):
    global cam_data
    cam_data = get_cams(cam_data)
    #schedule.every(3).minutes.do(func, cam_data)  #(get_cams(cams))
    #logger.info("run_get_cams_timer RUN")
    #while True:
        #schedule.run_pending()
        #time.sleep(1)

@repeat(schedule.every(5).minutes)
def run_operate_data_timer(): # (func):
    run_all()
    #schedule.every(5).minutes.do(func)  #(get_cams(cams))
    logger.info("run_operate_data_timer RUN")



if "__main__" == __name__:

    while True:
        schedule.run_pending()
        time.sleep(1)
    #threading.Thread(target=lambda: run_get_cams_timer(get_cams)).start()
    #threading.Thread(target=lambda: run_operate_data_timer(run_all)).start()

    #run_all()
    #print(cam_data)
    #t1 = parsing_data(test, cam)
    #t2 = change_data(cameras, cam_data)
    #print('cameras', cameras)
    #print(t2)
