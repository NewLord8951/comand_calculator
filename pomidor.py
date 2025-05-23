import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


class PomodoroTimer:
    def __init__(self, bot: Bot, chat_id: int):
        self.bot = bot
        self.chat_id = chat_id
        self.work_time = 25 * 60
        self.break_time = 5 * 60
        self.is_running = False
        self.current_task = None

    async def start_work(self):
        if self.is_running:
            return

        self.is_running = True
        await self.bot.send_message(self.chat_id, "🍅 Таймер Pomodoro запущен: 25 минут работы")

        await asyncio.sleep(self.work_time)
        if not self.is_running:
            return

        await self.bot.send_message(self.chat_id, "⏰ Время работы закончилось! Сделайте перерыв 5 минут")
        await self.start_break()

    async def start_break(self):
        await asyncio.sleep(self.break_time)
        if not self.is_running:
            return

        await self.bot.send_message(self.chat_id, "✅ Перерыв окончен. Можете начинать новый Pomodoro!")
        self.is_running = False

    def stop(self):
        self.is_running = False
        if self.current_task:
            self.current_task.cancel()


async def pomodoro_start(message: Message, bot: Bot):
    chat_id = message.chat.id
    timer = PomodoroTimer(bot, chat_id)
    global active_timers
    if chat_id in active_timers:
        active_timers[chat_id].stop()
    active_timers[chat_id] = timer
    asyncio.create_task(timer.start_work())
    await message.answer("🍅 Таймер Pomodoro запущен!")


async def pomodoro_stop(message: Message):
    chat_id = message.chat.id
    global active_timers
    if chat_id in active_timers:
        active_timers[chat_id].stop()
        del active_timers[chat_id]
        await message.answer("⏹ Таймер Pomodoro остановлен")
    else:
        await message.answer("ℹ️ Нет активных таймеров")

active_timers = {}


def setup_pomodoro(dp: Dispatcher):
    dp.message.register(pomodoro_start, Command("pomodoro"))
    dp.message.register(pomodoro_stop, Command("pomodorostop"))
