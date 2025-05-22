import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я Камкулятор 🧮\nОтправь мне \
        выражение, например: `5 + 3`")


@dp.message()
async def calculate(message: types.Message):
    try:
        # Разбиваем входное сообщение на части
        parts = message.text.split()
        if len(parts) != 3:
            await message.answer("Ошибка: Неверный \
                формат!\nИспользуйте формат: число \
                    оператор число\nНапример: `5 + 3`")
            return

        num1 = float(parts[0])
        operator = parts[1]
        num2 = float(parts[2])

        # Проверяем допустимость оператора
        if operator not in ['+', '-', '*', '/']:
            await message.answer("Ошибка: Неверный \
                оператор!\nДоступные операторы: +, -, *, /")
            return

        # Выполняем вычисление
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                await message.answer("Ошибка: Деление на ноль запрещено!")
                return
            result = num1 / num2

        # Отправляем результат
        await message.answer(f"{num1} {operator} {num2} = {result}")

    except ValueError:
        await message.answer("Ошибка: Пожалуйста, введите корректные числа!")
    except Exception as e:
        await message.answer("Произошла ошибка. Попробуй ещё раз.")
        print(e)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
