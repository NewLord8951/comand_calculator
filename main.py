import asyncio
import os
from loguru import logger
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from chat import numbers


dp = Dispatcher()

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")


async def main1():
    logger.add("file.log",
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
               rotation="3 days",
               backtrace=True,
               diagnose=True)

    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")

    numbers(dp)


if __name__ == '__main1__':
    asyncio.run(main1())
