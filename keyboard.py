from aiogram.types import ReplyKeyboardMarkup

calc_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
        ["C"]
    ],
    resize_keyboard=True
)
