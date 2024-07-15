from aiogram.fsm.state import StatesGroup, State


class botStates(StatesGroup):
    send_message_users = State()
