from aiogram.types import CallbackQuery

import wikipedia


async def callback_answer(callback_query: CallbackQuery):
    await callback_query.message.edit_text(f"{wikipedia.summary(callback_query.data)}")