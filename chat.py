import os
from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from keyboard import get_function_keyboard, get_answer_after_primer
from loguru import logger
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")


class Form(StatesGroup):
    first_number = State()
    second_number = State()


def numbers(dp: Dispatcher):
    @dp.message(Command('start'))
    async def cmd_start(message: types.Message, state: FSMContext):
        await state.set_state(Form.first_number)
        await message.answer("Здравствуйте, добро пожаловать в калькулятор!")
        await message.answer("Введите первое число")

    @dp.message(Form.first_number)
    async def process_first_number(message: types.Message, state: FSMContext):
        try:
            number = int(message.text)
            await state.update_data(first_number=number)
            await state.set_state(Form.second_number)
            await message.answer(f"Ваше первое число {number}. Введите второе число")
        except ValueError:
            await message.answer("Пожалуйста, введите корректное число (целое).")

    @dp.message(Form.second_number)
    async def process_second_number(message: types.Message, state: FSMContext):
        try:
            number = int(message.text)
            await state.update_data(second_number=number)
            data = await state.get_data()
            first = data['first_number']
            second = number
            await message.answer(
                f"Вы ввели два числа: {first} и {second}\nВыберите действие:",
                reply_markup=get_function_keyboard()
            )
        except ValueError:
            await message.answer("Пожалуйста, введите корректное число (целое).")

    # --- Операции ---

    @dp.message(F.text == "Сложение➕")
    async def handle_addition(message: types.Message, state: FSMContext):
        data = await state.get_data()

        if 'first_number' not in data or 'second_number' not in data:
            await message.answer("Пожалуйста, сначала введите оба числа.")
            return

        first = data['first_number']
        second = data['second_number']
        result = first + second

        await message.answer(f"Результат сложения {first} + {second} = {result}", reply_markup=get_answer_after_primer())

    @dp.message(F.text == "Вычитание➖")
    async def handle_subtraction(message: types.Message, state: FSMContext):
        data = await state.get_data()

        if 'first_number' not in data or 'second_number' not in data:
            await message.answer("Пожалуйста, сначала введите оба числа.")
            return

        first = data['first_number']
        second = data['second_number']
        result = first - second

        await message.answer(f"Результат вычитания {first} - {second} = {result}", reply_markup=get_answer_after_primer())

    @dp.message(F.text == "Умножение✖️")
    async def handle_multiplication(message: types.Message, state: FSMContext):
        data = await state.get_data()

        if 'first_number' not in data or 'second_number' not in data:
            await message.answer("Пожалуйста, сначала введите оба числа.")
            return

        first = data['first_number']
        second = data['second_number']
        result = first * second

        await message.answer(f"Результат умножения {first} × {second} = {result}", reply_markup=get_answer_after_primer())

    @dp.message(F.text == "Деление➗")
    async def handle_division(message: types.Message, state: FSMContext):
        data = await state.get_data()

        if 'first_number' not in data or 'second_number' not in data:
            await message.answer("Пожалуйста, сначала введите оба числа.")
            return

        first = data['first_number']
        second = data['second_number']

        if second == 0:
            await message.answer("Ошибка: деление на ноль невозможно!")
            return

        result = first / second
        await message.answer(f"Результат деления {first} ÷ {second} = {result}", reply_markup=get_answer_after_primer())

    # --- Логика продолжения ---

    @dp.message(F.text.in_({"Да✔", "Нет❌"}))
    async def handle_continue_choice(message: types.Message, state: FSMContext):
        if message.text == "Да✔":
            await state.set_state(Form.first_number)
            await message.answer("Введите первое число:", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer("Спасибо за использование калькулятора! До свидания!", reply_markup=ReplyKeyboardRemove())
            await state.clear()