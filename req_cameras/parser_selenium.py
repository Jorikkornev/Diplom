## Пример взят из сайта
# https://dev.to/bailon/how-to-set-up-selenium-as-a-linux-daemon-with-systemd-4bdc?
# ysclid=m3gzol4hqy631465664#installing-google-chrome
# TODO Создать функцию get_cameras_status() -> Dict | json | False - в случае ошибки +
# TODO Сделать комментарии к параметрам функции +/- взять из статьи
# https://yourtodo.ru/ru/posts/parsing-sajtov-s-ispolzovaniem-selenium-webdriver/
# TODO Добавить логирование и тесты +/- добавить тесты
# TODO Добавить логирование +
# TODO V 1.1 - протестировать запуск в отдельном потоке/на втором процессоре

import random
import time
from typing import List

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
## --------------------------- ##
from selenium.webdriver.chrome.service import Service
## ---- Use for type hint ---- ##
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

# Логгирование
import logging.config
from utils.logger import LOG_CONFIG

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


def create_chrome_web_driver_connection(headless: bool,
                                        detach: bool,
                                        use_sandbox: bool,
                                        use_dev_shm: bool,
                                        window_width: int = 1052,
                                        window_height: int = 825
                                        ) -> WebDriver:
    try:
        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", detach)
        options.add_argument(f"--window-size={window_width},{window_height}")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-renderer-backgrounding")
        options.page_load_strategy = 'normal'

        if not use_sandbox:
            options.add_argument('--no-sandbox')
        if not use_dev_shm:
            options.add_argument('--disable-dev-shm-usage')
        # Для экономии ресурсов - запуск без интерфейса
        if headless:
            options.add_argument("--headless=new")
        drv = webdriver.Chrome(service=service, options=options)
        logger.info('Driver start')
        return drv
    except Exception as e:
        logger.exception(f'Error: {e}', exc_info=False)


cams_l = []


def get_cams(cams: List) -> List:
    driver = create_chrome_web_driver_connection(headless=True,
                                                 detach=False,
                                                 use_sandbox=False,
                                                 use_dev_shm=False)
    if driver:
        try:
            driver.get('https://www.hik-connectru.com/views/login/index.html#/login')
            # https://www.hik-connectru.com/views/login/index.html#/login
            time.sleep(random.randrange(4, 6))
            field_account = driver.find_element(By.ID, 'basic_account')
            field_password = driver.find_element(By.ID, 'basic_password')
            field_account.send_keys('J.k0rnev@yandex.ru')
            time.sleep(random.randrange(2, 6))
            field_password.send_keys('Zw2SNqSz0y09')  # Zw2SNqSz0y09
            button_confirm = driver.find_element(By.CLASS_NAME, 'ant-btn-primary')
            time.sleep(random.randrange(4, 6))
            button_confirm.send_keys(Keys.RETURN)
            time.sleep(random.randrange(5, 10))
            driver.get('https://www.hik-connectru.com/views/login/index.html#/common/personal/OtherShareDevices')
            # https://www.hik-connectru.com/views/login/index.html#/common/personal/OtherShareDevices
            time.sleep(random.randrange(5, 10))
            # Получение списка камер
            find_cameras: list[WebElement] = driver.find_elements(By.CLASS_NAME, 'el-table__row')
            # el-table__row
            for find_camera in find_cameras:
                cams.append(find_camera.text)
            logger.info('Return cams')
            #print('cams: ', cams, type(cams))
            return cams
        except Exception as e:
            logger.exception(f'Error: {e}', exc_info=False)
        finally:
            driver.close()
            driver.quit()
            logger.info('Driver quit')
    else:
        logger.error('Selenium web driver Error')
        cams = []
        return cams


if "__main__" == __name__:
    test_cams = get_cams(cams_l)
    print(test_cams)
