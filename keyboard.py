from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging

logger = logging.getLogger(__name__)


def get_function_keyboard() -> ReplyKeyboardMarkup:
    try:
        buttons = [
            [KeyboardButton(text="Сложение➕"),
             KeyboardButton(text="Вычитание➖")],
            [KeyboardButton(text="Умножение✖️")],
            [KeyboardButton(text="Деление➗")]
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        logger.debug("Создана клавиатура выбора операции")
        return keyboard
    except Exception as e:
        logger.error(f"Ошибка при создании клавиатуры \
            операций: {e}", exc_info=True)
        raise


def get_answer_after_primer() -> ReplyKeyboardMarkup:
    try:
        buttons = [
            [KeyboardButton(text="Да✔"), KeyboardButton(text="Нет❌")]
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        logger.debug("Создана клавиатура подтверждения")
        return keyboard
    except Exception as e:
        logger.error(f"Ошибка при создании клавиатуры \
            подтверждения: {e}", exc_info=True)
        raise
