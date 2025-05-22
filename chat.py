import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from dotenv import find_dotenv, load_dotenv
import asyncio


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logger.error("Токен бота не найден! Проверьте файл .env")
    exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    try:
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        logger.info(f"Пользователь {user_name} (ID: {user_id}) запустил бота")

        welcome_text = (
            f"🔢 Привет, {user_name}! Я — бот-калькулятор. 🧮\n\n"
            "Просто напиши мне математическое выражение \
                (например, '2+2', '5*3' или '10/2'), "
            "и я мгновенно решу его! 😊\n\n"
        )
        await message.answer(welcome_text)
    except Exception as e:
        logger.error(f"Ошибка в команде start: {e}", exc_info=True)
        await message.answer("❌ Произошла ошибка при обработке команды")


@dp.message()
async def calculate(message: Message):
    try:
        user_id = message.from_user.id
        expression = message.text.strip()
        logger.info(f"Пользователь {user_id} отправил выражение: {expression}")

        # Ограничиваем допустимые символы для безопасности
        allowed_chars = set('0123456789+-*/(). ')
        if not set(expression).issubset(allowed_chars):
            await message.answer("⚠️ Введите только допустимые \
                математические символы!")
            return

        # Поддержка возведения в степень
        expression = expression.replace('^', '**')

        # Вычисление
        result = eval(expression)

        logger.info(f"Вычислено выражение: {expression} = {result}")
        await message.answer(f"✅ Результат: {result}")

    except ZeroDivisionError:
        logger.warning(f"Попытка деления на ноль: {expression}\
            (пользователь {user_id})")
        await message.answer("❌ Ошибка: деление на ноль!")
    except Exception as e:
        logger.error(f"Ошибка вычисления: {expression}\
            (пользователь {user_id}): {e}")
        await message.answer("❌ Ошибка: некорректный ввод. \
            Пример: '2+2' или '5*3'")


# --- Запуск бота ---
async def main():
    logger.info("Бот запущен и готов к работе...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
