from telegram.ext import CommandHandler
import threading
import time

def pomodoro_start(update, context):
    update.message.reply_text("🍅 Таймер Pomodoro запущен: 25 минут работы")
    
    def timer_callback():
        update.message.reply_text("⏰ Время работы закончилось! Сделайте перерыв 5 минут")
        # Запускаем таймер перерыва
        break_timer = threading.Timer(300, break_end, [update, context])
        break_timer.start()
    
    def break_end(update, context):
        update.message.reply_text("✅ Перерыв окончен. Можете начинать новый Pomodoro!")
    
    timer = threading.Timer(1500, timer_callback)
    timer.start()

def setup_pomodoro(dp):
    dp.add_handler(CommandHandler("pomodoro", pomodoro_start))