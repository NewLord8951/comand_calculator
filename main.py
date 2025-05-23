import asyncio
import os
from loguru import logger
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
import re
import math

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

calc_keyboard = [
    ['7', '8', '9', '/', '('],
    ['4', '5', '6', '*', ')'],
    ['1', '2', '3', '-', 'C'],
    ['0', '.', '=', '+', '⌫']
]


class CalcState(StatesGroup):
    normal = State()
    advanced = State()


@dp.message(Command('start'))
async def start_game(message: Message):
    await message.answer(
        f"Привет {message.from_user.first_name}! Я бот-калькулятор.\n"
        "Отправь мне математическое выражение или используй клавиатуру.\n"
        "Доступные команды:\n"
        "/calc - расширенный режим калькулятора",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=calc_keyboard,
            resize_keyboard=True
        )
    )


@dp.message()
async def handle_normal_mode(message: Message):
    text = message.text

    if text == 'C':
        await message.answer("Очищено. Введите новое выражение.")
        return

    if text == '=':
        await message.answer("Введите выражение перед нажатием '='")
        return

    if text == '⌫':
        await message.answer("Функция удаления пока не реализована")
        return

    try:
        cleaned_text = re.sub(r'[^\d+\-*/(). ]', '', text)
        result = eval(cleaned_text)
        await message.answer(f"Результат: {result}")
    except Exception as e:
        await message.answer(f"Ошибка: {e}\nПопробуйте еще раз.")


@dp.message(Command('calc'))
async def start_advanced_mode(message: Message, state: FSMContext):
    await state.set_state(CalcState.advanced)
    await message.answer(
        "📟 Расширенный режим калькулятора. Введите выражение:",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Command('cancel'), CalcState.advanced)
async def cancel_advanced_mode(message: Message, state: FSMContext):
    await state.set_state(CalcState.normal)
    await message.answer(
        "🚪 Выход из расширенного режима.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=calc_keyboard,
            resize_keyboard=True
        )
    )


@dp.message(CalcState.advanced)
async def handle_advanced_mode(message: Message, state: FSMContext):
    text = message.text
    try:
        cleaned_text = re.sub(r'[^\d+\-*/().^%&| ]', '', text)
        safe_dict = {k: v for k, v in math.__dict__.items() if not k.startswith('_')}
        safe_dict.update({'abs': abs, 'round': round})
        result = eval(cleaned_text, {"__builtins__": None}, safe_dict)
        await message.answer(
            f"✅ Результат: {result}\n\nВведите новое выражение или /cancel для выхода."
        )
    except Exception as e:
        await message.answer(
            f"❌ Ошибка: {e}\nПопробуйте еще раз или /cancel для выхода."
        )


async def main():
    logger.add(
        "file.log",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        rotation="3 days",
        backtrace=True,
        diagnose=True
    )

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

    logger.info("Бот запущен")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")

if __name__ == '__main__':
    asyncio.run(main())
