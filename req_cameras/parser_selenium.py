## Пример взят из сайта
# https://dev.to/bailon/how-to-set-up-selenium-as-a-linux-daemon-with-systemd-4bdc?
# ysclid=m3gzol4hqy631465664#installing-google-chrome
# TODO Создать функцию get_cameras_status() -> Dict | json | False - в случае ошибки
# TODO Сделать комментарии к параметрам функции
# TODO Добавить логирование и тесты
# TODO Добавить логирование
# TODO V 1.1 - протестировать запуск в отдельном потоке/на втором процессоре


# TODO Fix В режиме запуска без интерфейса часто появляется ошибка об отсутствии интернет подключения. Выяснить причину
#

import time
import random
from pprint import pprint

from selenium import webdriver
from selenium.webdriver import Keys
## ---- Use for type hint ---- ##
from selenium.webdriver.chrome.webdriver import WebDriver
## --------------------------- ##
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def create_chrome_web_driver_connection(headless: bool,
                                        detach: bool,
                                        use_sandbox: bool,
                                        use_dev_shm: bool,
                                        window_width: int = 1052,
                                        window_height: int = 825
                                        ) -> WebDriver:
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

    driver = webdriver.Chrome(service=service, options=options)

    return driver


if "__main__" == __name__:
    driver = create_chrome_web_driver_connection(headless=True,
                                                 detach=False,
                                                 use_sandbox=False,
                                                 use_dev_shm=False)

    driver.get('https://www.hik-connectru.com/views/login/index.html?country=114#/login')
    time.sleep(random.randrange(4, 6))
    field_account = driver.find_element(By.ID, 'basic_account')
    field_password = driver.find_element(By.ID, 'basic_password')
    field_account.send_keys('J.k0rnev@yandex.ru')
    time.sleep(random.randrange(2, 6))
    field_password.send_keys('5tRfshw$yU3W')
    button_confirm = driver.find_element(By.CLASS_NAME, 'ant-btn-primary')
    time.sleep(random.randrange(2, 6))
    print(button_confirm.text)
    button_confirm.send_keys(Keys.RETURN)
    time.sleep(random.randrange(5, 10))
    driver.get('https://www.hik-connectru.com/share/domains')
    data = driver.page_source
    # Декодируем данные
    #json_data = json.loads(data)
    pprint(data)
    #time.sleep(240)
    # Перейти на страницу с информацией по камерам https://www.hik-connectru.com/share/domains

    driver.close()
    driver.quit()
