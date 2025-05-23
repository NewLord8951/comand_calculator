from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import executor
from keyboard import calc_keyboard
import re

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher(bot)


async def start(message: types.Message):
    user = message.from_user
    await message.answer(
        f"Привет {user.first_name}! Я бот-калькулятор.\n"
        "Отправь мне математическое выражение или используй клавиатуру.\n"
        "Доступные команды:\n"
        "/calc - расширенный режим калькулятора",
        reply_markup=ReplyKeyboardMarkup(keyboard=calc_keyboard, resize_keyboard=True)
    )


async def handle_message(message: types.Message):
    text = message.text

    if text == 'C':
        await message.answer("Очищено. Введите новое выражение.")
        return

    if text == '=':
        await message.answer("Введите выражение перед нажатием '='")
        return

    try:
        cleaned_text = re.sub(r'[^\d+\-*/(). ]', '', text)
        result = eval(cleaned_text)
        await message.answer(f"Результат: {result}")
    except Exception as e:
        await message.answer(f"Ошибка: {e}\nПопробуйте еще раз.")

dp.register_message_handler(start, commands=['start'])
dp.register_message_handler(handle_message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
