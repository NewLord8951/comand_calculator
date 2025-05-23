from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.executor import Executor
import re
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(Command("start"))
await message.answer("...", reply_markup=calc_keyboard)
async def start(message: Message):
    user = message.from_user
    await message.answer("...", reply_markup=calc_keyboard)
    await message.answer(
        f"Привет {user.first_name}! Я бот-калькулятор.\n"
        "Отправь мне математическое выражение или используй клавиатуру.\n"
        "Доступные команды:\n"
        "/calc - расширенный режим калькулятора",
    )

# Обработчик обычных сообщений
@dp.message_handler()
async def handle_message(message: Message):
    text = message.text

    # Обработка специальных команд
    if text == 'C':
        await message.answer("Очищено. Введите новое выражение.")
        return

    if text == '=':
        await message.answer("Введите выражение перед нажатием '='")
        return

    try:
        # Безопасная проверка ввода
        if not re.match(r'^[\d+\-*/().\s]+$', text):
            raise ValueError("Недопустимые символы в выражении")
            
        result = eval(text)
        await message.answer(f"Результат: {result}")
    except Exception as e:
        logger.error(f"Ошибка вычисления: {e}")
        await message.answer(f"Ошибка: {e}\nПопробуйте еще раз.")

if __name__ == '__main__':
    # Запуск бота
    executor = Executor(dp)
    executor.start_polling()