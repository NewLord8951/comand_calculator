from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
from handler import start, handle_message
from chat import start_calc, calculate, cancel
import logging

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)
logger = logging.getLogger(__name__)

async def main():
    # Замените 'YOUR_BOT_TOKEN' на ваш токен
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('calc', start_calc)],
            states={
                0: [MessageHandler(filters.TEXT & ~filters.COMMAND, calculate)],
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )
    )
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())