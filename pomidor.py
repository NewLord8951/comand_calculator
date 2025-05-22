import os
from aiogram import Bot, Dispatcher
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv
from loguru import logger

# Настройка Loguru
logger.add("spy_bot.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | \
           {message}", level="INFO")
logger.add(
    "spy_bot.log", 
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="10 MB",  # Ротация логов при достижении 10 МБ
    compression="zip",  # Сжатие старых логов
    backtrace=True,  # Для детализации ошибок
    diagnose=True  # Подробная диагностика
)
# Загрузка конфига
load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not TOKEN:
    logger.error("Токен бота не найден! Проверьте .env файл")
    exit(1)

if not ADMIN_ID:
    logger.warning("ADMIN_ID не указан, бот будет только логировать данные")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message()
async def spy_on_user(message: Message):
    try:
        user = message.from_user
        log_data = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "text": message.text,
            "chat_id": message.chat.id,
            "message_id": message.message_id
        }

        # Детальное логирование
        logger.info(
            "Новое сообщение от {first_name} (ID: {user_id}): {text}",
            **log_data
        )

        # Отправка данных админу (если ADMIN_ID указан)
        if ADMIN_ID:
            try:
                await bot.send_message(
                    ADMIN_ID,
                    f"🕵️‍♂️ *Данные пользователя:*\n"
                    f"▫️ *ID:* `{user.id}`\n"
                    f"▫️ *Имя:* {user.first_name}\n"
                    f"▫️ *Фамилия:* {user.last_name}\n"
                    f"▫️ *Username:* @{user.username}\n"
                    f"▫️ *Текст:* `{message.text}`\n"
                    f"▫️ *Время:* {log_data['date']}",
                    parse_mode="Markdown"
                )
                logger.success(f"Данные отправлены админу (ID: {ADMIN_ID})")
            except Exception as admin_error:
                logger.error(f"Ошибка отправки админу: {admin_error}")

    except Exception as e:
        logger.exception(f"Критическая ошибка в spy_on_user: {e}")

if __name__ == '__main__':
    logger.info("🔄 Шпион-бот запущен")
    try:
        dp.run_polling(bot)
    except Exception as poll_error:
        logger.critical(f"Бот упал с ошибкой: {poll_error}")
    finally:
        logger.info("⏹ Бот остановлен")
