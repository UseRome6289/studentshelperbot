import re
import sqlite3

import requests
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import KeyBoards
import messages
from config import TOKEN
from utils import Register, Schedule, Change


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(state=Register.REGISTER_0)
async def register_1(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET real_name = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
    conn.commit()
    conn.close()
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(Register.all()[1])
    await message.reply(messages.institute_message, reply=False, reply_markup=KeyBoards.institute_kb)


@dp.message_handler(state=Change.CHANGE_0)
async def name_change(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET real_name = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
    conn.commit()
    conn.close()
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.reply(messages.end_of_registration_message
                        , reply=False, reply_markup=KeyBoards.menu_admin_kb)


@dp.message_handler(state=Register.REGISTER_1)
async def register_2(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET school = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
    conn.commit()
    conn.close()
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(Register.all()[2])
    await message.reply(messages.course_message, reply=False, reply_markup=KeyBoards.course_kb)


@dp.message_handler(state=Register.REGISTER_2)
async def register_2(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET course = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
    conn.commit()
    conn.close()
    state = dp.current_state(user=message.from_user.id)
    switch_text = message.text.lower()
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT chat_id, school, course FROM users")
    result_set = cursor.fetchall()
    for i in result_set:
        if i[0] == message.from_user.id:
            # ИКИТ
            if i[1] == "ИКИТ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.ikit_kb)
            elif i[1] == "ИКИТ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.ikit_kb)
            elif i[1] == "ИКИТ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.ikit_kb)
            elif i[1] == "ИКИТ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.ikit_kb)
            elif i[1] == "ИКИТ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.ikit_kb)
            # ИУБП
            elif i[1] == "ИУБП" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИУБП" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИУБП" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИУБП" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИУБП" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИФБИБТ
            elif i[1] == "ИФБиБТ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИФБиБТ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИФБиБТ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИФБиБТ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИФБиБТ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИФИЯК
            elif i[1] == "ИФиЯК" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИФиЯК" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИФиЯК" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИФиЯК" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИФиЯК" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ВУЦ
            elif i[1] == "ВУЦ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ВУЦ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ВУЦ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ВУЦ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ВУЦ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ГИ
            elif i[1] == "ГИ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ГИ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ГИ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ГИ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ГИ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИСИ
            elif i[1] == "ИСИ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИСИ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИСИ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИСИ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИСИ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИНИГ
            elif i[1] == "ИНиГ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИНиГ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИНиГ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИНиГ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИНиГ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИАИД
            elif i[1] == "ИАиД" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИАиД" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИАиД" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИАиД" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИАиД" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИГДГиГ
            elif i[1] == "ИГДГиГ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИГДГиГ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИГДГиГ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИГДГиГ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИГДГиГ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИИФиРЭ
            elif i[1] == "ИИФиРЭ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИИФиРЭ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИИФиРЭ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИИФиРЭ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИИФиРЭ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИМИФИ
            elif i[1] == "ИМиФИ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИМиФИ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИМиФИ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИМиФИ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИМиФИ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИППС
            elif i[1] == "ИППС" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИППС" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИППС" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИППС" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИППС" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИФКСИТ
            elif i[1] == "ИФКСиТ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИФКСиТ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИФКСиТ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИФКСиТ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИФКСиТ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИЦМИМ
            elif i[1] == "ИЦМиМ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИЦМиМ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИЦМиМ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИЦМиМ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИЦМиМ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИЭИГ
            elif i[1] == "ИЭиГ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИЭиГ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИЭиГ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИЭиГ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИЭиГ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИГ
            elif i[1] == "ИГ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИГ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИГ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИГ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИГ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИТИСУ
            elif i[1] == "ИТиСУ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИТиСУ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИТиСУ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИТиСУ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИТиСУ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ИЭУИФ
            elif i[1] == "ИЭУиФ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИЭУиФ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИЭУиФ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИЭУиФ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ИЭУиФ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ПИ
            elif i[1] == "ПИ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ПИ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ПИ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ПИ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ПИ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            # ЮИ
            elif i[1] == "ЮИ" and i[2] == "1 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ЮИ" and i[2] == "2 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ЮИ" and i[2] == "3 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ЮИ" and i[2] == "4 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)
            elif i[1] == "ЮИ" and i[2] == "5 курс":
                await state.set_state(Register.all()[3])
                await message.reply(messages.group_message, reply=False, reply_markup=KeyBoards.gi_kb)

    conn.commit()
    conn.close()


@dp.message_handler(state=Register.REGISTER_3)
async def register_3(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET user_group = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
    conn.commit()
    conn.close()
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    # Здесь нужно раздавать права на админ панель
    await message.reply(messages.end_of_registration_message
                        , reply=False, reply_markup=KeyBoards.menu_admin_kb)


@dp.message_handler(state=Schedule.TEST_STATE_0)
async def schedule_1(msg: types.Message):
    timetable_message = ""
    current_week = "0"
    url = 'https://edu.sfu-kras.ru/timetable'
    response = requests.get(url).text
    if msg.text != 'Меню':
        match = re.search(r'Идёт\s\w{8}\sнеделя', response)
        if match:
            timetable_message += "Сейчас идёт <b>нечётная</b> неделя\n"
            current_week = "1"
        else:
            timetable_message += "Сейчас идёт <b>чётная</b> неделя\n"
            current_week = "2"
        url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={msg.text}')
        response = requests.get(url).json()
        for item in response["timetable"]:
            if item["week"] == current_week:
                timetable_message += f"\n{item['day'].replace('1', '<b>Понедельник</b>').replace('2', '<b>Вторник</b>').replace('3', '<b>Среда</b>').replace('4', '<b>Четверг</b>').replace('5', '<b>Пятница</b>').replace('6', '<b>Суббота</b>')}" \
                                     f"\n{item['time']}\n{item['subject']}\n{item['type']}\n" \
                                     f"{item['teacher']}\n{item['place']}\n"
        await msg.reply(timetable_message, parse_mode="HTML")
    state = dp.current_state(user=msg.from_user.id)
    await state.reset_state()
    await msg.reply('Главное меню', reply=False, reply_markup=KeyBoards.menu_admin_kb)


@dp.message_handler(commands='start')
async def process_start_command(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users(chat_id, name) values ({message.from_user.id}, '{message.from_user.username}')")
    conn.commit()
    conn.close()

    await message.reply(f'Доброго времени суток!, {message.from_user.username}.\n'
                        '\n Это наш StudentHelperBot, здесь всегда можно узнать актуальное расписание, поставить '
                        'напоминания, подписаться на рассылки: чат группы, сообщения от преподавателей, у нас есть свои'
                        ' PevCoin\'ы (валюта в разработке)\n Регаемся?)', reply_markup=KeyBoards.greet_kb)


@dp.message_handler(commands='help')
async def process_start2_command(message: types.Message):
    await message.reply(f'Доброго времени суток!, {message.from_user.username}.\n'
                        '\n Это наш StudentHelperBot, здесь всегда можно узнать актуальное расписание, поставить '
                        'напоминания, подписаться на рассылки: чат группы, сообщения от преподавателей и многое другое!'
                        'Для управлением бота, используйте кнопки.'
                        , reply_markup=KeyBoards.menu_admin_kb)


@dp.message_handler(state='*', content_types=["text"])
async def handler_message(msg: types.Message):
    global adding
    global group
    switch_text = msg.text.lower()
    if switch_text == "расписание":
        await msg.reply(":: Выберите день недели ::", reply_markup=KeyBoards.day_of_the_week_kb)

    elif switch_text == "понедельник":
        timetable_message = ""
        current_week = "0"
        url = 'https://edu.sfu-kras.ru/timetable'
        response = requests.get(url).text
        match = re.search(r'Идёт\s\w{8}\sнеделя', response)
        if match:
            current_week = "1"
        else:
            current_week = "2"
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, user_group FROM users")
        result_set = cursor.fetchall()
        for i in result_set:
            if i[0] == msg.from_user.id:
                group = i[1]
        url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
        response = requests.get(url).json()
        adding = []
        for item in response["timetable"]:
            if item["week"] == current_week:
                adding.append(
                    [item['day'], item['time'], item['subject'], item['type'], item['teacher'], item['place']])
        flag = 0
        for i in adding:
            if i[0] == '1':
                if i[2] != '':
                    flag = 1
        if flag == 1:
            if match:
                timetable_message += "Сейчас идёт <b>нечётная</b> неделя\n"
            else:
                timetable_message += "Сейчас идёт <b>чётная</b> неделя\n"
            timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Понедельник</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
            for i in adding:
                if i[0] == '1':
                    if i[4] == '' and i[5] == '':
                        timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                    else:
                        timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
        else:
            timetable_message += 'Пар нет!\n Отличный повод увидеться с друзьями!'
        await msg.reply(timetable_message, parse_mode="HTML")

    elif switch_text == "вторник":
        timetable_message = ""
        current_week = "0"
        url = 'https://edu.sfu-kras.ru/timetable'
        response = requests.get(url).text
        match = re.search(r'Идёт\s\w{8}\sнеделя', response)
        if match:
            current_week = "1"
        else:
            current_week = "2"
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, user_group FROM users")
        result_set = cursor.fetchall()
        for i in result_set:
            if i[0] == msg.from_user.id:
                group = i[1]
        url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
        response = requests.get(url).json()
        adding = []
        for item in response["timetable"]:
            if item["week"] == current_week:
                adding.append(
                    [item['day'], item['time'], item['subject'], item['type'], item['teacher'], item['place']])
        flag = 0
        for i in adding:
            if i[0] == '2':
                if i[2] != '':
                    flag = 1
        if flag == 1:
            if match:
                timetable_message += "Сейчас идёт <b>нечётная</b> неделя\n"
            else:
                timetable_message += "Сейчас идёт <b>чётная</b> неделя\n"
            timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Вторник</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
            for i in adding:
                if i[0] == '2':
                    if i[4] == '' and i[5] == '':
                        timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                    else:
                        timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
        else:
            timetable_message += 'Пар нет! Отличный повод увидеться с друзьями!'
        await msg.reply(timetable_message, parse_mode="HTML")

    elif switch_text == "среда":
        timetable_message = ""
        current_week = "0"
        url = 'https://edu.sfu-kras.ru/timetable'
        response = requests.get(url).text
        match = re.search(r'Идёт\s\w{8}\sнеделя', response)
        if match:
            current_week = "1"
        else:
            current_week = "2"
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, user_group FROM users")
        result_set = cursor.fetchall()
        for i in result_set:
            if i[0] == msg.from_user.id:
                group = i[1]
        url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
        response = requests.get(url).json()
        adding = []
        for item in response["timetable"]:
            if item["week"] == current_week:
                adding.append(
                    [item['day'], item['time'], item['subject'], item['type'], item['teacher'], item['place']])
        flag = 0
        for i in adding:
            if i[0] == '3':
                if i[2] != '':
                    flag = 1
        if flag == 1:
            if match:
                timetable_message += "Сейчас идёт <b>нечётная</b> неделя\n"
            else:
                timetable_message += "Сейчас идёт <b>чётная</b> неделя\n"
            timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Среда</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
            for i in adding:
                if i[0] == '3':
                    if i[4] == '' and i[5] == '':
                        timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                    else:
                        timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
        else:
            timetable_message += 'Пар нет! Отличный повод увидеться с друзьями!'
        await msg.reply(timetable_message, parse_mode="HTML")

    elif switch_text == "четверг":
        timetable_message = ""
        current_week = "0"
        url = 'https://edu.sfu-kras.ru/timetable'
        response = requests.get(url).text
        match = re.search(r'Идёт\s\w{8}\sнеделя', response)
        if match:
            current_week = "1"
        else:
            current_week = "2"
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, user_group FROM users")
        result_set = cursor.fetchall()
        for i in result_set:
            if i[0] == msg.from_user.id:
                group = i[1]
        url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
        response = requests.get(url).json()
        adding = []
        for item in response["timetable"]:
            if item["week"] == current_week:
                adding.append(
                    [item['day'], item['time'], item['subject'], item['type'], item['teacher'], item['place']])
        flag = 0
        for i in adding:
            if i[0] == '4':
                if i[2] != '':
                    flag = 1
        if flag == 1:
            if match:
                timetable_message += "Сейчас идёт <b>нечётная</b> неделя\n"
            else:
                timetable_message += "Сейчас идёт <b>чётная</b> неделя\n"
            timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Четверг</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
            for i in adding:
                if i[0] == '4':
                    if i[4] == '' and i[5] == '':
                        timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                    else:
                        timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
        else:
            timetable_message += 'Пар нет! Отличный повод увидеться с друзьями!'
        await msg.reply(timetable_message, parse_mode="HTML")

    elif switch_text == "пятница":
        timetable_message = ""
        current_week = "0"
        url = 'https://edu.sfu-kras.ru/timetable'
        response = requests.get(url).text
        match = re.search(r'Идёт\s\w{8}\sнеделя', response)
        if match:
            current_week = "1"
        else:
            current_week = "2"
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, user_group FROM users")
        result_set = cursor.fetchall()
        for i in result_set:
            if i[0] == msg.from_user.id:
                group = i[1]
        url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
        response = requests.get(url).json()
        adding = []
        for item in response["timetable"]:
            if item["week"] == current_week:
                adding.append(
                    [item['day'], item['time'], item['subject'], item['type'], item['teacher'], item['place']])
        flag = 0
        for i in adding:
            if i[0] == '5':
                if i[2] != '':
                    flag = 1
        if flag == 1:
            if match:
                timetable_message += "Сейчас идёт <b>нечётная</b> неделя\n"
            else:
                timetable_message += "Сейчас идёт <b>чётная</b> неделя\n"
            timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Пятница</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
            for i in adding:
                if i[0] == '5':
                    if i[4] == '' and i[5] == '':
                        timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                    else:
                        timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
        else:
            timetable_message += 'Пар нет! Отличный повод увидеться с друзьями!'
        await msg.reply(timetable_message, parse_mode="HTML")

    elif switch_text == "суббота":
        timetable_message = ""
        current_week = "0"
        url = 'https://edu.sfu-kras.ru/timetable'
        response = requests.get(url).text
        match = re.search(r'Идёт\s\w{8}\sнеделя', response)
        if match:
            current_week = "1"
        else:
            current_week = "2"
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, user_group FROM users")
        result_set = cursor.fetchall()
        for i in result_set:
            if i[0] == msg.from_user.id:
                group = i[1]
        url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
        response = requests.get(url).json()
        adding = []
        for item in response["timetable"]:
            if item["week"] == current_week:
                adding.append(
                    [item['day'], item['time'], item['subject'], item['type'], item['teacher'], item['place']])
        flag = 0
        for i in adding:
            if i[0] == '6':
                if i[2] != '':
                    flag = 1
        if flag == 1:
            if match:
                timetable_message += "Сейчас идёт <b>нечётная</b> неделя\n"
            else:
                timetable_message += "Сейчас идёт <b>чётная</b> неделя\n"
            timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Суббота</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
            for i in adding:
                if i[0] == '6':
                    if i[4] == '' and i[5] == '':
                        timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                    else:
                        timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
        else:
            timetable_message += 'Пар нет! Отличный повод увидеться с друзьями!'
        await msg.reply(timetable_message, parse_mode="HTML")
    # Регистрация
    elif switch_text == "регистрация":
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(Register.all()[0])
        await msg.reply("Введите ваше ФИО:")

    elif switch_text == "админ-панель":
        await msg.reply("-Раз-ра-бот-ка-", reply_markup=KeyBoards.admin_panel)

    elif switch_text == "меню":
        await msg.reply(":: Вы в меню ::", reply_markup=KeyBoards.menu_admin_kb)

    elif switch_text == "рассылки":
        await msg.reply(":: Ваши полученные рассылки ::", reply_markup=KeyBoards.mailing_lists_kb)

    elif switch_text == "профиль":
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, real_name, user_group FROM users")
        result_set = cursor.fetchall()
        for i in result_set:
            if i[0] == msg.from_user.id:
                await bot.send_message(msg.from_user.id, f"Ваше ФИО: {i[1]}\n"
                                                         f"Ваша группа: {i[2]}")
        conn.commit()
        conn.close()
    elif switch_text == "чат":
        await msg.reply("-Раз-ра-бот-ка-", reply_markup=KeyBoards.chat_kb)

    elif switch_text == "настройки":
        await msg.reply(":: Вы в настройках ::", reply_markup=KeyBoards.setting_kb)

    elif switch_text == "запланированные мероприятия":
        await msg.reply(":: Ваши мероприятия ::", reply_markup=KeyBoards.events_kb)

    elif switch_text == "изменить информацию":
        await msg.reply("-Раз-ра-бот-ка-", reply_markup=KeyBoards.change_information_kb)

    elif switch_text == "добавить мероприятие":
        await msg.reply("Введите ваше мероприятие:", reply_markup=KeyBoards.universal_kb)

    elif switch_text == "назад":
        await msg.reply(":: Вы в настройках ::", reply_markup=KeyBoards.setting_kb)

    # Изменение имени
    elif switch_text == "изменить имя":
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, real_name FROM users")
        result_set = cursor.fetchall()
        for i in result_set:
            if i[0] == msg.from_user.id:
                await bot.send_message(msg.from_user.id, f"Ваше ФИО: {i[1]}\n")
        conn.commit()
        conn.close()
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(Change.all()[0])
        await bot.send_message(msg.from_user.id, ":: Введите ваше имя ::")
    # Изменение группы
    elif switch_text == "изменить группу":
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, user_group, school, course FROM users")
        result_set = cursor.fetchall()
        for i in result_set:
            if i[0] == msg.from_user.id:
                await bot.send_message(msg.from_user.id,
                                       f"Ваш институт: {i[2]}\nВаш курс: {i[3]}\nВаша группа: {i[1]}\n")
        conn.commit()
        conn.close()
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(Register.all()[1])
        await msg.reply(":: Выберите ваш институт ::", reply_markup=KeyBoards.institute_kb)

    elif switch_text == "посмотреть расписание другой группы":
        await msg.reply(":: Введите группу: ::", reply_markup=KeyBoards.universal_kb)
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(Schedule.all()[0])

    elif switch_text == "поддержка разработчиков":
        await msg.reply("Разработчики программы:\n\t1.Шульц Илья\n\t2.Присяжнюк Кирилл\n\t3.Степанцов Антон"
                        , reply_markup=KeyBoards.universal_kb)


if __name__ == "__main__":
    executor.start_polling(dp, on_shutdown=shutdown)
