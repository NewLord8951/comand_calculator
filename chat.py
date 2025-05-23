from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import re
import math


class CalcStates(StatesGroup):
    CALCULATING = State()


async def start_calc(message: types.Message, state: FSMContext):
    await message.answer(
        "📟 Расширенный режим калькулятора. Введите выражение:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(CalcStates.CALCULATING)


async def calculate(message: types.Message, state: FSMContext):
    text = message.text
    try:
        cleaned_text = re.sub(r'[^\d+\-*/().^%&| ]', '', text)
        safe_dict = {k: v for k, v in globals().items() if k in dir(__builtins__) or k in dir(math)}
        result = eval(cleaned_text, {"__builtins__": None}, safe_dict)
        await message.answer(
            f"✅ Результат: {result}\n\nВведите новое выражение или /cancel для выхода."
        )
    except Exception as e:
        await message.answer(
            f"❌ Ошибка: {e}\nПопробуйте еще раз или /cancel для выхода."
        )


async def cancel(message: types.Message, state: FSMContext):
    from keyboard import calc_keyboard

    await message.answer(
        "🚪 Выход из расширенного режима.",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=calc_keyboard,
            resize_keyboard=True
        )
    )
    await state.clear()


def setup_calculator(dp: Dispatcher):
    dp.message.register(start_calc, Command("calc"))
    dp.message.register(cancel, Command("cancel"), CalcStates.CALCULATING)
    dp.message.register(calculate, CalcStates.CALCULATING)
