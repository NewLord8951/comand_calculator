from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, MessageHandler, filters
import re

async def start_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📟 Расширенный режим калькулятора. Введите выражение:",
        reply_markup=ReplyKeyboardRemove()
    )
    return 0

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        cleaned_text = re.sub(r'[^\d+\-*/(). ]', '', text)
        result = eval(cleaned_text)
        await update.message.reply_text(
            f"✅ Результат: {result}\n\nВведите новое выражение или /cancel для выхода."
        )
        return 0
    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {e}\nПопробуйте еще раз или /cancel для выхода."
        )
        return 0

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from keyboard import calc_keyboard
    from telegram import ReplyKeyboardMarkup
    
    await update.message.reply_text(
        "🚪 Выход из расширенного режима.",
        reply_markup=ReplyKeyboardMarkup(calc_keyboard, resize_keyboard=True)
    )
    return ConversationHandler.END