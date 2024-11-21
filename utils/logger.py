# TODO ограничить размер файла лога
formatters = {
    'file_formatter': {
        'format': '[{levelname}: {asctime}] [{filename}:{funcName}:{lineno}]: "{message}"',
        'style': '{'
    },
    'debug_formatter': {
        'format': '[{levelname}] [{filename}:{funcName}:{lineno}]: "{message}"',
        'style': '{'
    },
}

handlers = {
    'console_handler': {  # имя обработчика
        'level': 'DEBUG',  # уровень сообщений на который начнет реагировать обработчик
        'class': 'logging.StreamHandler',
        'formatter': 'debug_formatter',  # указываем как форматировать сообщение
        'stream': 'ext://sys.stdout'
        # По умолчанию stderr. Этот параметр указан, чтобы в консоли вывод был простым белым шрифтом, как в print, а не красным, как будто это ошибки.
    },
    'file_handler': {
        'level': 'INFO',
        'class': 'logging.FileHandler',
        'formatter': 'file_formatter',
        'filename': '../logs/debug.log',
        # путь до лог файла. Без разницы какая ОС: Windows, Linux записываем через '/'
        'mode': 'a',
        # По умолчанию 'a'. Режим записи, все как у обычногого файла. 'a' дозапись в текущий файл. 'w' новый файл, предыдущие записи стираются
        'encoding': 'utf-8',  # кодировка
    },
}

modules_and_level = (
    ('__main__', 'DEBUG'),
    ('req_cameras.parser_selenium', 'INFO'),
    ('req_cameras.create_data', 'INFO'),
    #('common.utils', 'DEBUG'),
    #('common.common', 'INFO'),
    #('execute', 'DEBUG')
)

loggers = {}

for logger in modules_and_level:
    loggers[logger[0]] = {
        'handlers': ['console_handler', 'file_handler'],
        'level': logger[1],
        'propagate': False
    }

LOG_CONFIG = {
    'version': 1,  # обязательный параметр
    'formatters': formatters,
    'handlers': handlers,
    'loggers': loggers
}

# TODO Добавить отправку ошибок в ТГ
"""
    # обработчик Telegram
class TelegramBotHandler(Handler): 
    def __init__(self, token: str, chat_id: str): 
    super().__init__() 
    self.token = token 
    self.chat_id = chat_id 
    def emit(self, record: LogRecord) -> None: 
    url = f'https://api.telegram.org/bot{self.token}/sendMessage' 
    post_data = {'chat_id': self.chat_id, 
    'text': self.format(record)} 
    http = urllib3.PoolManager() 
    http.request(method='POST', url=url, fields=post_data)
    # обработчик Telegram
    
    # В handlers
    'telegram_handler': { 
        'class': 'settings.TelegramBotHandler', # здесь указываем созданный нами обработчик Telegram
        'level': 'INFO', 
        'token': TELEGRAM_BOT_TOKEN, 
        'chat_id': TELEGRAM_CHAT_ID 
    }
    # В handlers
    
"""