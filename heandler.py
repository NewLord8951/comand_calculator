from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from keyboard import calc_keyboard
import re

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет {user.first_name}! Я бот-калькулятор.\n"
        "Отправь мне математическое выражение или используй клавиатуру.\n"
        "Доступные команды:\n"
        "/calc - расширенный режим калькулятора",
        reply_markup=ReplyKeyboardMarkup(calc_keyboard, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == 'C':
        await update.message.reply_text("Очищено. Введите новое выражение.")
        return
    
    if text == '=':
        await update.message.reply_text("Введите выражение перед нажатием '='")
        return
    
    try:
        cleaned_text = re.sub(r'[^\d+\-*/(). ]', '', text)
        result = eval(cleaned_text)
        await update.message.reply_text(f"Результат: {result}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}\nПопробуйте еще раз.")