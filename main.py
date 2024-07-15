from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand
from aiogram.filters import Command

from states import botStates
import functions
import callback_functions
import datas

from asyncio import run

dp = Dispatcher()


async def main():
    dp.startup.register(functions.start_up_answer)
    dp.shutdown.register(functions.shut_down_answer)

    dp.message.register(functions.start_command_answer, Command("start"))
    dp.message.register(functions.send_message_all_users, botStates.send_message_users)
    dp.message.register(functions.admin_answer, F.from_user.id == datas.admin_id)
    dp.message.register(functions.wiki_answer)
    dp.callback_query.register(callback_functions.callback_answer)

    bot = Bot(token=datas.token)

    await bot.set_my_commands([
        BotCommand(command="/start", description="Botni ishga tushurish")
    ])

    await dp.start_polling(bot)


run(main())
