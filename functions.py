from aiogram.types import Message
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError

import keyboards
import datas
from states import botStates

import wikipedia
import json

wikipedia.set_lang('uz')


async def start_up_answer(bot: Bot):
    await bot.send_message(datas.admin_id, "Bot ishga tushdi ✅")


async def shut_down_answer(bot: Bot):
    await bot.send_message(datas.admin_id, "Bot ishdan to'xtadi ❗️")


async def start_command_answer(message: Message, bot: Bot, state: FSMContext):
    if message.from_user.id == datas.admin_id:
        await message.answer("Assalomu aleykum ADMIN", reply_markup=keyboards.send_message_button)
    else:
        await message.answer(
            f"Assalomu aleykum, {message.from_user.first_name}. Botga xush kelibsiz, ushbu botda sizga o'zbek "
            f"tilidagi wikipedia ma'lumotlarini olishingizga yordam beradi. \nBoshlash uchun ma'lumot olmoqchi "
            f"bo'lgan mavzuingizni kiriting"
        )

    with open("users.json") as file:
        data = json.load(file)

    user_id = str(message.from_user.id)

    if user_id not in data["active_users"].keys():
        data["active_users"][user_id] = {}
    if user_id in data["passive_users"].keys():
        del data["passive_users"][user_id]
    if user_id not in data["all_users"].keys():
        data["all_users"][user_id] = {}
        matn = f"NEW {message.from_user.mention_html("USER")}:\nID {message.from_user.id}"
        user = await bot.get_chat(message.from_user.id)
        user_photos = await message.from_user.get_profile_photos()
        if user.bio: matn += f"\nBio: {user.bio}"
        if message.from_user.username: matn += f"\nUsername: @{message.from_user.username}"
        if user_photos.photos:
            await bot.send_photo(datas.admin_id, user_photos.photos[0][-1].file_id, caption=matn, parse_mode="HTML")
        else:
            await bot.send_message(datas.admin_id, matn, parse_mode="HTML")
    with open("users.json", "w") as file:
        json.dump(data, file, indent=4)


async def admin_answer(message: Message, state: FSMContext):
    with open("users.json") as file:
        data = json.load(file)

    if message.text == "SEND MESSAGE":
        await message.answer("Yubormoqchi bo'lgan xabaringizni kiriting kiriting:")
        await state.set_state(botStates.send_message_users)

    elif message.text == "USERS":
        text = (f"ALL USER: {len(data["all_users"].keys())}\n"
                f"ACTIVE USER: {len(data["active_users"].keys())}\n"
                f"PASSIVE USER: {len(data["passive_users"].keys())}")
        await message.answer(text)

    else:
        search_results = wikipedia.search(message.text, results=10)
        if search_results:
            await message.answer(f"{message.text.capitalize()} bo'yicha qidiruv natijalari:",
                                 reply_markup=keyboards.add_button(search_results))
        else:
            await message.answer(f"{message.text.capitalize()} bo'yicha ma'lumot topilmadi")


async def wiki_answer(message: Message, state: FSMContext):
    search_results = wikipedia.search(message.text, results=10)
    if search_results:
        await message.answer(f"{message.text.capitalize()} bo'yicha qidiruv natijalari:",
                             reply_markup=keyboards.add_button(search_results))
    else:
        await message.answer(f"{message.text.capitalize()} bo'yicha ma'lumot topilmadi")


async def send_message_all_users(message: Message, bot: Bot, state: FSMContext):
    with open("users.json") as file:
        data = json.load(file)

    for user in data["all_users"].keys():
        try:
            await message.copy_to(user)
            if user in data["passive_users"].keys():
                del data["passive_users"][user]
            if user not in data["active_users"].keys():
                data["active_users"][user] = {}
        except TelegramForbiddenError:
            if user in data["active_users"].keys():
                del data["active_users"][user]
            if user not in data["passive_users"].keys():
                data["passive_users"][user] = {}

    await bot.send_message(data["admin_id"], "Xabar jo'natildi", reply_markup=keyboards.send_message_button)
    await state.clear()

    with open("users.json", "w") as file:
        json.dump(data, file, indent=4)
