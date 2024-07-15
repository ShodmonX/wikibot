from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def add_button(message):

    search_results_buttons = InlineKeyboardBuilder()
    for i in message:
        search_results_buttons.button(text=i, callback_data=i)

    search_results_buttons.adjust(1, repeat=True)
    return search_results_buttons.as_markup()


send_message_button = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="SEND MESSAGE"),
        KeyboardButton(text="USERS")
    ]
],
    resize_keyboard=True
)
