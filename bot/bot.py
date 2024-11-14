# TODO На этапе разработки и тестирования всё находится в одном проекте
# TODO После проверки работоспособности, вынести бот в отдельный проект - V 1.0
# TODO Разработать получение данных - Redis, httprequest, MQQT?

import asyncio
from aiogram import Bot, Dispatcher
from handlers import rt_questions, different_types
from config_reader import config


# Запуск бота
async def main():
    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(rt_questions.router, different_types.router)

    # Альтернативный вариант регистрации роутеров по одному на строку
    # dp.include_router(questions.router)
    # dp.include_router(different_types.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())