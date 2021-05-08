# region imports
import datetime
import re
import sqlite3
import threading
import time
from threading import Thread

import requests
import telebot
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.types import ContentType, ReplyKeyboardMarkup
from aiogram.utils import executor

import KeyBoards
import messages
from config import TOKEN, PAYMENTS_PROVIDER_TOKEN, TIME_MACHINE_IMAGE_URL
from messages import MESSAGES
from utils import Register, Change, Pay, AdminPanel, ScheduleUser, Events, Schedule, CheckSchedule, Delete


# endregion


# region global
async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


bot2 = telebot.TeleBot(__name__)
bot2.config['api_key'] = TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

incoming_events = {}
incoming_events2 = {}
incoming_event3 = {}
incoming_inst = []

def only_letters(tested_string):
    for letter in tested_string:
        if letter not in KeyBoards.alphabet:
            return False
    return True


class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global adding
        while not self.stopped.wait(3):
            conn = sqlite3.connect('db.db')

            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `times` WHERE `time` <=  strftime('%s', 'now') + 1800;")
            result_set30 = cursor.fetchall()
            for item in result_set30:
                cursor.execute(f"SELECT `real_name` FROM `users` WHERE `chat_id` = {item[0]}")
                real_name = cursor.fetchall()
                cursor.execute(f"SELECT `30min` FROM `times` WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                state = cursor.fetchall()
                if state[0][0] == 1:
                    cursor.execute(
                        f"UPDATE `times` SET `30min`= {0} WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                    bot2.send_message(item[0], f'{real_name[0][0]}! Мероприятие: {item[1]} состоится через пол часа')

            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `times` WHERE `time` <=  strftime('%s', 'now') + 300;")
            result_set5 = cursor.fetchall()
            for item in result_set5:
                cursor.execute(f"SELECT `real_name` FROM `users` WHERE `chat_id` = {item[0]}")
                real_name = cursor.fetchall()
                cursor.execute(f"SELECT `5min` FROM `times` WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                state = cursor.fetchall()
                if state[0][0] == 1:
                    cursor.execute(
                        f"UPDATE `times` SET `5min`= {0} WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                    bot2.send_message(item[0], f'{real_name[0][0]}! Мероприятие: {item[1]} состоится через пять минут')

            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `times` WHERE `time` <=  strftime('%s', 'now');")
            result_set = cursor.fetchall()
            cursor.execute(f"DELETE FROM `times` WHERE `time` <=  strftime('%s', 'now');")
            conn.commit()
            for item in result_set:
                cursor.execute(f"SELECT `real_name` FROM `users` WHERE `chat_id` = {item[0]}")
                real_name = cursor.fetchall()
                bot2.send_message(item[0], f'{real_name[0][0]}! Ваше мероприятие: {item[1]}\nокончено')

            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `mail` WHERE `time` <=  strftime('%s', 'now') + 1800;")
            result_set30 = cursor.fetchall()
            for item in result_set30:
                cursor.execute(f"SELECT `real_name` FROM `users` WHERE `chat_id` = {item[0]}")
                real_name = cursor.fetchall()
                cursor.execute(f"SELECT `30min` FROM `mail` WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                state = cursor.fetchall()
                if state[0][0] == 1:
                    cursor.execute(
                        f"UPDATE `mail` SET `30min`= {0} WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                    bot2.send_message(item[0], f'{real_name[0][0]}! Рассылка: {item[1]} состоится через пол часа')

            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `mail` WHERE `time` <=  strftime('%s', 'now') + 300;")
            result_set5 = cursor.fetchall()
            for item in result_set5:
                cursor.execute(f"SELECT `real_name` FROM `users` WHERE `chat_id` = {item[0]}")
                real_name = cursor.fetchall()
                cursor.execute(f"SELECT `5min` FROM `mail` WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                state = cursor.fetchall()
                if state[0][0] == 1:
                    cursor.execute(
                        f"UPDATE `mail` SET `5min`= {0} WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                    bot2.send_message(item[0], f'{real_name[0][0]}! Рассылка: {item[1]} состоится через пять минут')

            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `mail` WHERE `time` <=  strftime('%s', 'now');")
            result_set_del = cursor.fetchall()
            cursor.execute(f"DELETE FROM `mail` WHERE `time` <=  strftime('%s', 'now');")
            conn.commit()
            conn.close()
            for item in result_set_del:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT `real_name` FROM `users` WHERE `chat_id` = {item[0]}")
                real_name = cursor.fetchall()
                conn.commit()
                conn.close()
                bot2.send_message(item[0], f'{real_name[0][0]}! Рассылка: {item[1]} закончилась')


class MyThread2(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global adding
        while not self.stopped.wait(60):
            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "1"
            else:
                current_week = "2"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT user_group FROM users")
            result_set = cursor.fetchall()

            cursor.close()
            listing = []
            for i in result_set:
                listing.append(i)
            listing = list(set(listing))
            for i in listing:
                url = f'http://edu.sfu-kras.ru/api/timetable/get?target={i[0]}'
                response = requests.get(url).json()
                adding = []
                date = datetime.datetime.today()
                date_date = date.strftime('%H:%M')
                date_split = date_date.split(':')
                listing_date_split = []
                for n in date_split:
                    n = int(n)
                    listing_date_split.append(n)
                listing_date_sum = listing_date_split[0] * 60 + listing_date_split[1]
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
                date1 = datetime.datetime.today()
                now = datetime.datetime.weekday(date1) + 1
                for j in adding:
                    if int(j[0]) == now:
                        a = j[1].split('-')
                        if date_date == a[0]:
                            conn = sqlite3.connect('db.db')
                            cursor = conn.cursor()
                            cursor.execute(f"SELECT chat_id, real_name FROM users WHERE user_group = '{i[0]}'")
                            id_group = cursor.fetchall()
                            cursor.close()
                            for k in id_group:
                                if j[5] == "":
                                    bot2.send_message(k[0], f'{k[1]}, у вас начался {j[2]}')
                                else:
                                    bot2.send_message(k[0], f'{k[1]}, у вас начался {j[2]} в {j[5]}')
                        date_kur = a[0].split(':')
                        listing_date = []
                        for n in date_kur:
                            n = int(n)
                            listing_date.append(n)
                        listing_date_sum2 = listing_date[0] * 60 + listing_date[1]
                        if listing_date_sum == listing_date_sum2 - 5:
                            conn = sqlite3.connect('db.db')
                            cursor = conn.cursor()
                            cursor.execute(f"SELECT chat_id, real_name FROM users WHERE user_group = '{i[0]}'")
                            id_group = cursor.fetchall()
                            cursor.close()
                            for k in id_group:
                                if j[5] == "":
                                    bot2.send_message(k[0], f'{k[1]}, у вас через 5 минут начнется {j[2]}')
                                else:
                                    bot2.send_message(k[0], f'{k[1]}, у вас начнется {j[2]} через 5 минут в {j[5]}')


# endregions


@dp.message_handler(state='*', commands='start')
async def process_start_command(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users(chat_id, name) values ({message.from_user.id}, '{message.from_user.username}')")
    conn.commit()
    conn.close()
    if message.from_user.username != None:
        await message.reply(f'Welcome to StudentHelperBot, {message.from_user.username}!🔥\n'
                            '\n - Here you can always find the current schedule 🎓'
                            '\n - Set reminders 🍻'
                            '\n - Mailing lists from teachers ✉'
                            '\n - View the current schedule of another group ✌'
                            '\n - Support developers 👌'
                            '\n - We have our own PevCoin (currency in development) 💵'
                            '\n'
                            '\n  Registering? ✨'
                            '\n'
                            '\n ➖➖➖➖➖➖'
                            '\n'
                            '\n'
                            f'Добро пожаловать в StudentHelperBot, {message.from_user.username}!🔥\n'
                            '\n - Здесь всегда можно узнать актуальное расписание 🎓'
                            '\n - Поставить напоминания 🍻'
                            '\n - Рассылки от преподавателей ✉'
                            '\n - Посмотреть актуальное расписание другой группы ✌'
                            '\n - Поддержать разработчиков 👌'
                            '\n - У нас есть свои PevCoin\'ы (валюта в разработке) 💵'
                            '\n'
                            ' \n  Регистрируемся? ✨', reply_markup=KeyBoards.greet_kb)
    else:
        await message.reply(messages.greets_msg, reply_markup=KeyBoards.greet_kb)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(Register.all()[0])


# region userHandler
@dp.message_handler(state=Events.EVENTS_USER_0)
async def process_command0(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()

    else:
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(Events.all()[1])
        incoming_events[message.from_user.id] = message.text
        await message.reply(messages.events
                            , reply_markup=KeyBoards.time_kb)


@dp.message_handler(state=Events.EVENTS_USER_1)
async def process_command1(message: types.Message):
    global timing
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        m = {'1 час': 60 * 60, "2 часа": 60 * 60 * 2, "3 часа": 60 * 60 * 3, "4 часа": 60 * 60 * 4,
             "5 часов": 60 * 60 * 5,
             "18 часов": 60 * 60 * 18, "6 часов": 60 * 60 * 6, "12 часов": 60 * 60 * 12,
             "24 часа": 60 * 60 * 24,
             "2 дня": 60 * 60 * 48, "3 дня": 60 * 60 * 24 * 3, "Неделя": 60 * 60 * 24 * 7}
        try:
            if m[message.text]:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(
                    f"INSERT INTO times(`chat_id`, `event1`, `time`, `30min`, `5min`) values ({message.from_user.id}, '{incoming_events[message.from_user.id]}', {round(time.time() + m[message.text])}, {1}, {1})")
                incoming_events.pop(message.from_user.id)
                conn.commit()
                conn.close()
                is_succeed = False
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_id FROM admins")
                result_set = cursor.fetchall()
                cursor.close()
                for item in result_set:
                    if item[0] == message.from_user.id:
                        is_succeed = True
                if is_succeed:
                    await message.reply(messages.successfully
                                        , reply=False, reply_markup=KeyBoards.menu_admin_kb)
                    conn.commit()
                    conn.close()
                    state = dp.current_state(user=message.from_user.id)
                    await state.reset_state()
                else:
                    await message.reply(messages.successfully
                                        , reply=False, reply_markup=KeyBoards.menu_user_kb)
                    conn.commit()
                    conn.close()
                    state = dp.current_state(user=message.from_user.id)
                    await state.reset_state()
        except KeyError:
            await bot.send_message(message.from_user.id, messages.message_error4)


# endregion


# region adminHandler
@dp.message_handler(state=AdminPanel.ADMIN_0)
async def process_admin_command2(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()

    elif switch_text == 'отправить рассылку':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(AdminPanel.all()[1])
        await message.reply(messages.write_mail, reply_markup=KeyBoards.return_keyboard)
    elif switch_text == 'отправить рассылку всем пользователям':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(AdminPanel.all()[6])
        await message.reply(messages.write_mail, reply_markup=KeyBoards.return_keyboard)
    else:
        await bot.send_message(message.from_user.id, messages.what)


@dp.message_handler(state=AdminPanel.ADMIN_1)
async def process_admin_command1(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        if only_letters(message.text) == True:
            cursor.execute(
                f"UPDATE admins SET last_content = '{message.text}' WHERE user_id = '{message.from_user.id}'")
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(AdminPanel.all()[2])
            await message.reply(messages.university, reply_markup=KeyBoards.institute_kb)
        else:
            await bot.send_message(message.from_user.id, messages.message_error5)


@dp.message_handler(state=AdminPanel.ADMIN_2)
async def process_admin_command4(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        try:
            if messages.institutes[message.text]:
                if only_letters(message.text) == True:
                    conn = sqlite3.connect('db.db')
                    cursor = conn.cursor()
                    cursor.execute(
                        f"UPDATE admins SET inst = '{messages.institutes[message.text]}' WHERE user_id = '{message.from_user.id}'")
                    conn.commit()
                    cursor.execute(f"SELECT inst FROM admins WHERE user_id = '{message.from_user.id}'")
                    inst = cursor.fetchall()[0][0]
                    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
                    url = 'https://edu.sfu-kras.ru/api/timetable/groups'
                    response = requests.get(url).json()
                    for item in response:
                        if item['institute'] == inst:
                            keyboard.add(item['name'])
                            incoming_inst.append(item['name'])
                    await message.reply(messages.group_message, reply_markup=keyboard)
                    state = dp.current_state(user=message.from_user.id)
                    await state.set_state(AdminPanel.all()[3])
                else:
                    await bot.send_message(message.from_user.id, messages.message_error)
        except KeyError:
            await bot.send_message(message.from_user.id, messages.message_error)


@dp.message_handler(state=AdminPanel.ADMIN_3)
async def process_admin_command4(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        a = False
        for i in incoming_inst:
            if i == message.text:
                a = True
        if only_letters(message.text) == True:
            if a == True:
                incoming_inst.clear()
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE admins SET `group` = '{message.text}' WHERE user_id = '{message.from_user.id}'")
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(AdminPanel.all()[4])
                await message.reply(messages.timer, reply=False, reply_markup=KeyBoards.time_kb2)
            else:
                await bot.send_message(message.from_user.id, messages.message_error6)
        else:
            await bot.send_message(message.from_user.id, messages.message_error6)


@dp.message_handler(state=AdminPanel.ADMIN_4)
async def process_admin_command4(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        m = {'Без таймера': 10, '1 час': 60 * 60, "2 часа": 60 * 60 * 2, "3 часа": 60 * 60 * 3, "4 часа": 60 * 60 * 4,
             "5 часов": 60 * 60 * 5,
             "18 часов": 60 * 60 * 18, "6 часов": 60 * 60 * 6, "12 часов": 60 * 60 * 12,
             "24 часа": 60 * 60 * 24,
             "2 дня": 60 * 60 * 48, "3 дня": 60 * 60 * 24 * 3, "Неделя": 60 * 60 * 24 * 7}
        try:
            if m[message.text]:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                if message.text != 'Без таймера':
                    cursor.execute(
                        f"UPDATE admins SET `time` = '{round(time.time() + m[message.text])}' WHERE user_id = '{message.from_user.id}'")
                    incoming_event3[message.from_user.id] = message.text
                else:
                    cursor.execute(
                        f"UPDATE admins SET `time` = '{10}' WHERE user_id = '{message.from_user.id}'")
                    incoming_event3[message.from_user.id] = message.text
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(AdminPanel.all()[5])
                await message.reply(messages.mailing, reply=False, reply_markup=KeyBoards.
                                    yes_or_no_keyboard)
        except KeyError:
            await bot.send_message(message.from_user.id, messages.message_error4)


@dp.message_handler(state=AdminPanel.ADMIN_5)
async def process_admin_command1(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    elif switch_text == 'да':
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id FROM users")
        id_users = cursor.fetchall()
        cursor.close()
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT last_content FROM admins WHERE user_id = '{message.from_user.id}'")
        content = cursor.fetchall()
        cursor.execute(f"SELECT `group` FROM admins WHERE user_id = '{message.from_user.id}'")
        group = cursor.fetchall()
        cursor.execute(f"SELECT `real_name` FROM users WHERE chat_id = '{message.from_user.id}'")
        name = cursor.fetchall()
        cursor.execute(f"SELECT `time` FROM admins WHERE user_id = '{message.from_user.id}'")
        time2 = cursor.fetchall()
        cursor.close()
        for user in id_users:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT `user_group` FROM users WHERE chat_id = '{user[0]}'")
            group_users = cursor.fetchall()
            cursor.close()
            if group_users == group:
                try:
                    a = f'Рассылка от пользователя: <b>{name[0][0]}</b>\n' + f'<i>{content[0][0]}</i>'
                    if incoming_event3[message.from_user.id] == 'Без таймера':
                        incoming_event3.pop(message.from_user.id)
                    else:
                        incoming_event3.pop(message.from_user.id)
                        conn = sqlite3.connect('db.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            f"INSERT INTO mail(`chat_id`, `event1`, `time`, `30min`, `5min`) values ({user[0]}, '{content[0][0]}', {time2[0][0]}, {1}, {1})")

                        conn.commit()
                        conn.close()
                    await dp.bot.send_message(user[0], a, parse_mode='HTML')
                except:
                    pass
        await dp.bot.send_message(message.from_user.id,
                                  f'Ваша рассылка: <b>{content[0][0]}</b>\nУспешно отправлена группе '
                                  f'<b>{group[0][0]}</b>', parse_mode='HTML')
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(AdminPanel.all()[2])
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.successfully
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.successfully
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()

    elif switch_text == 'изменить':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(AdminPanel.all()[0])
        await message.reply("Выберите действие ✨", reply_markup=KeyBoards.admin_panel)


@dp.message_handler(state=AdminPanel.ADMIN_6)
async def process_admin_command1(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        if only_letters(message.text) == True:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE admins SET last_content = '{message.text}' WHERE user_id = '{message.from_user.id}'")
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(AdminPanel.all()[7])
            await message.reply(messages.timer, reply_markup=KeyBoards.time_kb2)
        else:
            await bot.send_message(message.from_user.id, messages.message_error5)


@dp.message_handler(state=AdminPanel.ADMIN_7)
async def process_admin_command4(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        m = {'Без таймера': 10, '1 час': 60 * 60, "2 часа": 60 * 60 * 2, "3 часа": 60 * 60 * 3, "4 часа": 60 * 60 * 4,
             "5 часов": 60 * 60 * 5,
             "18 часов": 60 * 60 * 18, "6 часов": 60 * 60 * 6, "12 часов": 60 * 60 * 12,
             "24 часа": 60 * 60 * 24,
             "2 дня": 60 * 60 * 48, "3 дня": 60 * 60 * 24 * 3, "Неделя": 60 * 60 * 24 * 7}
        try:
            if m[message.text]:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                if message.text != 'Без таймера':
                    cursor.execute(
                        f"UPDATE admins SET `time` = '{round(time.time() + m[message.text])}' WHERE user_id = '{message.from_user.id}'")
                    incoming_event3[message.from_user.id] = message.text
                else:
                    cursor.execute(
                        f"UPDATE admins SET `time` = '{0}' WHERE user_id = '{message.from_user.id}'")
                    incoming_event3[message.from_user.id] = message.text
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(AdminPanel.all()[8])
                await message.reply(messages.mailing, reply=False, reply_markup=KeyBoards.
                                    yes_or_no_keyboard)
        except KeyError:
            await bot.send_message(message.from_user.id, messages.message_error4)


@dp.message_handler(state=AdminPanel.ADMIN_8)
async def process_admin_command1(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    elif switch_text == 'да':
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id FROM users")
        id_users = cursor.fetchall()
        cursor.close()
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT last_content FROM admins WHERE user_id = '{message.from_user.id}'")
        content = cursor.fetchall()
        cursor.execute(f"SELECT `real_name` FROM users WHERE chat_id = '{message.from_user.id}'")
        name = cursor.fetchall()
        cursor.execute(f"SELECT `time` FROM admins WHERE user_id = '{message.from_user.id}'")
        time2 = cursor.fetchall()
        cursor.close()
        for user in id_users:
            try:
                a = f'Рассылка от пользователя: <b>{name[0][0]}</b>\n' + '\n ➖➖➖➖➖➖ \n\n' + f'<i>{content[0][0]}</i>'
                if incoming_event3[message.from_user.id] != 'Без таймера':
                    conn = sqlite3.connect('db.db')
                    cursor = conn.cursor()
                    cursor.execute(
                        f"INSERT INTO mail(`chat_id`, `event1`, `time`, `30min`, `5min`) values ({user[0]}, "
                        f"'{content[0][0]}', {time2[0][0]}, {1}, {1})")

                    conn.commit()
                    conn.close()
                await dp.bot.send_message(user[0], a, parse_mode='HTML')
            except:
                pass
        incoming_event3.pop(message.from_user.id)
        await dp.bot.send_message(message.from_user.id,
                                  f'Ваша рассылка: <b>{content[0][0]}</b>\nУспешно отправлена всем!'
                                  , parse_mode='HTML')
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(AdminPanel.all()[2])
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.successfully
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.successfully
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()

    elif switch_text == 'изменить':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(AdminPanel.all()[0])
        await message.reply(messages.choose_action, reply_markup=KeyBoards.admin_panel)


# endregion

# region payHandler
@dp.message_handler(state=Pay.PAY_DISTRIBUTOR)
async def process_buy_command0(message: types.Message):
    switch_text = message.text.lower()
    if message.text == 'Меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    elif message.text == 'Узнать команду разработчиков':
        await message.reply(messages.admin, parse_mode="HTML",
                            reply_markup=KeyBoards.developer_support_kb)
    elif message.text == 'Поддержать разработку телеграмм-бота':
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(Pay.all()[1])
        await message.reply(messages.thanks
                            , reply_markup=KeyBoards.developer_support_kb2)
    else:
        await bot.send_message(message.from_user.id, messages.what)


@dp.message_handler(state=Pay.PAY_DISTRIBUTOR2)
async def process_buy_command01(message: types.Message):
    switch_text = message.text.lower()
    if message.text == 'Меню':
        state = dp.current_state(user=message.from_user.id)
        await state.reset_state()
        await message.reply(messages.menu, reply_markup=KeyBoards.menu_admin_kb)
    elif switch_text == "поддержать разработчиков 100 рублей":
        if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
            await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])
        await bot.send_invoice(message.chat.id,
                               title=MESSAGES['tm_title'],
                               description=MESSAGES['tm_description'],
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='rub',
                               photo_url=TIME_MACHINE_IMAGE_URL,
                               photo_height=512,  # !=0/None, иначе изображение не покажется
                               photo_width=512,
                               photo_size=512,
                               is_flexible=False,  # True если конечная цена зависит от способа доставки
                               prices=[KeyBoards.PRICE100],
                               start_parameter='developer-support',
                               payload='some-invoice-payload-for-our-internal-use'
                               )
    elif switch_text == "поддержать разработчиков 250 рублей":
        if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
            await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])
        await bot.send_invoice(message.chat.id,
                               title=MESSAGES['tm_title'],
                               description=MESSAGES['tm_description'],
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='rub',
                               photo_url=TIME_MACHINE_IMAGE_URL,
                               photo_height=512,  # !=0/None, иначе изображение не покажется
                               photo_width=512,
                               photo_size=512,
                               is_flexible=False,  # True если конечная цена зависит от способа доставки
                               prices=[KeyBoards.PRICE250],
                               start_parameter='developer-support',
                               payload='some-invoice-payload-for-our-internal-use'
                               )
    elif switch_text == "поддержать разработчиков 500 рублей":
        if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
            await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])
        await bot.send_invoice(message.chat.id,
                               title=MESSAGES['tm_title'],
                               description=MESSAGES['tm_description'],
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='rub',
                               photo_url=TIME_MACHINE_IMAGE_URL,
                               photo_height=512,  # !=0/None, иначе изображение не покажется
                               photo_width=512,
                               photo_size=512,
                               is_flexible=False,  # True если конечная цена зависит от способа доставки
                               prices=[KeyBoards.PRICE500],
                               start_parameter='developer-support',
                               payload='some-invoice-payload-for-our-internal-use'
                               )
    elif switch_text == "поддержать разработчиков 1000 рублей":
        if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
            await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])
        await bot.send_invoice(message.chat.id,
                               title=MESSAGES['tm_title'],
                               description=MESSAGES['tm_description'],
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='rub',
                               photo_url=TIME_MACHINE_IMAGE_URL,
                               photo_height=512,  # !=0/None, иначе изображение не покажется
                               photo_width=512,
                               photo_size=512,
                               is_flexible=False,  # True если конечная цена зависит от способа доставки
                               prices=[KeyBoards.PRICE1000],
                               start_parameter='developer-support',
                               payload='some-invoice-payload-for-our-internal-use'
                               )
    elif switch_text == "поддержать разработчиков другой суммой":
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(Pay.all()[2])
        await bot.send_message(message.from_user.id, messages.summa)
    else:
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(Pay.all()[1])
        await bot.send_message(message.from_user.id, messages.wrong)


@dp.message_handler(state=Pay.PAY_DISTRIBUTOR3)
async def process_buy_command01(message: types.Message):
    switch_text = message.text.lower()
    if message.text == 'Меню':
        state = dp.current_state(user=message.from_user.id)
        await state.reset_state()
        await message.reply(messages.menu, reply_markup=KeyBoards.menu_admin_kb)
    elif switch_text == "поддержать разработчиков 100 рублей":
        if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
            await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])
        await bot.send_invoice(message.chat.id,
                               title=MESSAGES['tm_title'],
                               description=MESSAGES['tm_description'],
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='rub',
                               photo_url=TIME_MACHINE_IMAGE_URL,
                               photo_height=512,  # !=0/None, иначе изображение не покажется
                               photo_width=512,
                               photo_size=512,
                               is_flexible=False,  # True если конечная цена зависит от способа доставки
                               prices=[KeyBoards.PRICE100],
                               start_parameter='developer-support',
                               payload='some-invoice-payload-for-our-internal-use'
                               )
    elif switch_text == "поддержать разработчиков 250 рублей":
        if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
            await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])
        await bot.send_invoice(message.chat.id,
                               title=MESSAGES['tm_title'],
                               description=MESSAGES['tm_description'],
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='rub',
                               photo_url=TIME_MACHINE_IMAGE_URL,
                               photo_height=512,  # !=0/None, иначе изображение не покажется
                               photo_width=512,
                               photo_size=512,
                               is_flexible=False,  # True если конечная цена зависит от способа доставки
                               prices=[KeyBoards.PRICE250],
                               start_parameter='developer-support',
                               payload='some-invoice-payload-for-our-internal-use'
                               )
    elif switch_text == "поддержать разработчиков 500 рублей":
        if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
            await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])
        await bot.send_invoice(message.chat.id,
                               title=MESSAGES['tm_title'],
                               description=MESSAGES['tm_description'],
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='rub',
                               photo_url=TIME_MACHINE_IMAGE_URL,
                               photo_height=512,  # !=0/None, иначе изображение не покажется
                               photo_width=512,
                               photo_size=512,
                               is_flexible=False,  # True если конечная цена зависит от способа доставки
                               prices=[KeyBoards.PRICE500],
                               start_parameter='developer-support',
                               payload='some-invoice-payload-for-our-internal-use'
                               )
    elif switch_text == "поддержать разработчиков 1000 рублей":
        if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
            await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])
        await bot.send_invoice(message.chat.id,
                               title=MESSAGES['tm_title'],
                               description=MESSAGES['tm_description'],
                               provider_token=PAYMENTS_PROVIDER_TOKEN,
                               currency='rub',
                               photo_url=TIME_MACHINE_IMAGE_URL,
                               photo_height=512,  # !=0/None, иначе изображение не покажется
                               photo_width=512,
                               photo_size=512,
                               is_flexible=False,  # True если конечная цена зависит от способа доставки
                               prices=[KeyBoards.PRICE1000],
                               start_parameter='developer-support',
                               payload='some-invoice-payload-for-our-internal-use'
                               )
    elif switch_text == "поддержать разработчиков другой суммой":
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(Pay.all()[2])
        await bot.send_message(message.from_user.id, messages.summa)
    else:
        if message.text.isdigit() == True:
            if (int(message.text) >= 80 and message.text.isdigit() == True and int(message.text) <= 100000):
                integer = int(message.text)
                pr = integer * 100
                price = types.LabeledPrice(label='Поддержать разработчиков другой суммой', amount=pr)
                if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
                    await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])
                await bot.send_invoice(message.chat.id,
                                       title=MESSAGES['tm_title'],
                                       description=MESSAGES['tm_description'],
                                       provider_token=PAYMENTS_PROVIDER_TOKEN,
                                       currency='rub',
                                       photo_url=TIME_MACHINE_IMAGE_URL,
                                       photo_height=512,  # !=0/None, иначе изображение не покажется
                                       photo_width=512,
                                       photo_size=512,
                                       is_flexible=False,  # True если конечная цена зависит от способа доставки
                                       prices=[price],
                                       start_parameter='developer-support',
                                       payload='some-invoice-payload-for-our-internal-use'
                                       )
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Pay.all()[1])
            else:
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Pay.all()[1])
                await bot.send_message(message.from_user.id, messages.wrong)
        else:
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(Pay.all()[1])
            await bot.send_message(message.from_user.id, messages.wrong)


# endregion payHandler


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(
            total_amount=message.successful_payment.total_amount // 100,
            currency=message.successful_payment.currency
        )
    )
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.reply(messages.menu, reply_markup=KeyBoards.menu_admin_kb)


@dp.message_handler(state=Change.CHANGE_0)
async def name_change(message: types.Message):
    switch_text = message.text.lower()
    if only_letters(message.text) == True:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET real_name = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        await bot.send_message(message.from_user.id, messages.message_error2)


# region registerHandler

# start
@dp.message_handler(state=Register.REGISTER_0)
async def register_1(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == "я студент":
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(Register.all()[1])
        await message.reply(messages.student_name)
    elif switch_text == "я преподаватель":
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(Register.all()[4])
        await message.reply(messages.teacher_surname)


# name
@dp.message_handler(state=Register.REGISTER_1)
async def register_2(message: types.Message):
    if only_letters(message.text) == True:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET real_name = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
        conn.commit()
        conn.close()
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(Register.all()[2])
        await message.reply(messages.institute_message, reply=False, reply_markup=KeyBoards.institute_kb)
    else:
        await bot.send_message(message.from_user.id, messages.message_error2)


# inst
@dp.message_handler(state=Register.REGISTER_2)
async def register_2(message: types.Message):
    try:
        if messages.institutes[message.text]:
            if only_letters(message.text) == True:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(
                    f"UPDATE users SET school = '{messages.institutes[message.text]}' WHERE chat_id = '{message.from_user.id}'")
                conn.commit()
                cursor.execute(f"SELECT school FROM users WHERE chat_id = '{message.from_user.id}'")
                inst = cursor.fetchall()[0][0]
                keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
                url = 'https://edu.sfu-kras.ru/api/timetable/groups'
                response = requests.get(url).json()
                for item in response:
                    if item['institute'] == inst:
                        keyboard.add(item['name'])
                        incoming_inst.append(item['name'])
                await message.reply(messages.group_message, reply_markup=keyboard)
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Register.all()[3])
            else:
                await bot.send_message(message.from_user.id, messages.message_error)
    except KeyError:
        await bot.send_message(message.from_user.id, messages.message_error)


# group
@dp.message_handler(state=Register.REGISTER_3)
async def register_3(message: types.Message):
    a = False
    for i in incoming_inst:
        if i == message.text:
            a = True
    if only_letters(message.text) == True:
        if a == True:
            incoming_inst.clear()
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET user_group = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
            cursor.execute(f"SELECT user_id FROM admins")
            result_set = cursor.fetchall()
            cursor.close()
            is_succeed = False
            for item in result_set:
                if item[0] == message.from_user.id:
                    is_succeed = True
            if is_succeed:
                await message.reply(messages.end_of_registration_message
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.end_of_registration_message
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        else:
            await bot.send_message(message.from_user.id, messages.message_error6)
    else:
        await bot.send_message(message.from_user.id, messages.message_error6)


@dp.message_handler(state=Register.REGISTER_4)
async def register_4(message: types.message):
    url = "http://edu.sfu-kras.ru/timetable/teachers/autocomplete/"
    surname = message.text
    response = requests.get(url + surname).json()
    keyboard = ReplyKeyboardMarkup()
    if len(response) != 0:
        for item in response:
            keyboard.add(item)
            incoming_inst.append(item)
        await message.reply(messages.select, reply_markup=keyboard)
        await dp.current_state(user=message.from_user.id).set_state(Register.all()[5])
    else:
        await message.reply(messages.error, reply_markup=keyboard)


@dp.message_handler(state=Register.REGISTER_5)
async def register_5(message: types.message):
    a = False
    for i in incoming_inst:
        if i == message.text:
            a = True
    if only_letters(message.text) == True:
        if a == True:
            incoming_inst.clear()
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET real_name = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
            cursor.execute(f"UPDATE users SET user_group = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
            cursor.execute(f"UPDATE users SET is_teacher = '{True}' WHERE chat_id = '{message.from_user.id}'")
            cursor.execute(f"SELECT user_id FROM admins")
            result_set = cursor.fetchall()
            cursor.close()
            is_succeed = False
            for item in result_set:
                if item[0] == message.from_user.id:
                    is_succeed = True
            if is_succeed:
                await message.reply(messages.end_of_registration_message
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.end_of_registration_message
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        else:
            await bot.send_message(message.from_user.id, messages.message_error3)
    else:
        await bot.send_message(message.from_user.id, messages.message_error3)


# endregion


# region schedule_userHandler
@dp.message_handler(state=ScheduleUser.SCHEDULE_USER_0)
async def schedule_0(msg: types.Message):
    try:
        if messages.institutes[msg.text]:
            if only_letters(msg.text) == True:
                inst = messages.institutes[msg.text]
                keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")
                url = 'https://edu.sfu-kras.ru/api/timetable/groups'
                response = requests.get(url).json()
                for item in response:
                    if item['institute'] == inst:
                        keyboard.add(item['name'])
                        incoming_inst.append(item['name'])
                await msg.reply(messages.group_message, reply_markup=keyboard)
                state = dp.current_state(user=msg.from_user.id)
                await state.set_state(ScheduleUser.all()[1])
            else:
                await bot.send_message(msg.from_user.id, messages.message_error)
    except KeyError:
        await bot.send_message(msg.from_user.id, messages.message_error)


@dp.message_handler(state=ScheduleUser.SCHEDULE_USER_1)
async def schedule_1(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        a = False
        for i in incoming_inst:
            if i == message.text:
                a = True
        if only_letters(message.text) == True:
            if a == True:
                incoming_inst.clear()
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(
                    f"INSERT INTO user_table(chat_id) values ({message.from_user.id})")
                cursor.execute(
                    f"UPDATE user_table SET user_group = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
                conn.commit()
                conn.close()
                await message.reply(messages.day_of_the_week, reply_markup=KeyBoards.day_of_the_week_kb)
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(ScheduleUser.all()[2])
            else:
                await bot.send_message(message.from_user.id, messages.message_error6)
        else:
            await bot.send_message(message.from_user.id, messages.message_error6)


@dp.message_handler(state=ScheduleUser.SCHEDULE_USER_2)
async def schedule_1(message: types.Message):
    global group
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        if switch_text == "понедельник":
            timetable_message = ""
            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "1"
            else:
                current_week = "2"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT chat_id, user_group FROM user_table")
            result_set = cursor.fetchall()
            cursor.close()
            for i in result_set:
                if i[0] == message.from_user.id:
                    group = i[1]
            url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
            response = requests.get(url).json()
            adding = []
            for item in response["timetable"]:
                if item["week"] == current_week:
                    adding.append(
                        [item['day'], item['time'], item['subject'], "", item['type'], item['place']])
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
                timetable_message += 'В понедельник у этой группы пар нет!'
            await message.reply(timetable_message, parse_mode="HTML")

        elif switch_text == "вторник":
            timetable_message = ""

            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "1"
            else:
                current_week = "2"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT chat_id, user_group FROM user_table")
            result_set = cursor.fetchall()
            cursor.close()
            for i in result_set:
                if i[0] == message.from_user.id:
                    group = i[1]
            url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
            response = requests.get(url).json()
            adding = []
            for item in response["timetable"]:
                if item["week"] == current_week:
                    adding.append(
                        [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
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
                timetable_message += 'Во вторник у этой группы пар нет!'
            await message.reply(timetable_message, parse_mode="HTML")

        elif switch_text == "среда":
            timetable_message = ""

            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "1"
            else:
                current_week = "2"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT chat_id, user_group FROM user_table")
            result_set = cursor.fetchall()
            cursor.close()
            for i in result_set:
                if i[0] == message.from_user.id:
                    group = i[1]
            url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
            response = requests.get(url).json()
            adding = []
            for item in response["timetable"]:
                if item["week"] == current_week:
                    adding.append(
                        [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
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
                timetable_message += 'В среду у этой группы пар нет!'
            await message.reply(timetable_message, parse_mode="HTML")

        elif switch_text == "четверг":
            timetable_message = ""

            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "1"
            else:
                current_week = "2"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT chat_id, user_group FROM user_table")
            result_set = cursor.fetchall()
            cursor.close()
            for i in result_set:
                if i[0] == message.from_user.id:
                    group = i[1]
            url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
            response = requests.get(url).json()
            adding = []
            for item in response["timetable"]:
                if item["week"] == current_week:
                    adding.append(
                        [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
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
                timetable_message += 'В четверг у этой группы пар нет!'
            await message.reply(timetable_message, parse_mode="HTML")

        elif switch_text == "пятница":
            timetable_message = ""

            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "1"
            else:
                current_week = "2"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT chat_id, user_group FROM user_table")
            result_set = cursor.fetchall()
            cursor.close()
            for i in result_set:
                if i[0] == message.from_user.id:
                    group = i[1]
            url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
            response = requests.get(url).json()
            adding = []
            for item in response["timetable"]:
                if item["week"] == current_week:
                    adding.append(
                        [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
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
                timetable_message += 'В пятницу у этой группы пар нет!'
            await message.reply(timetable_message, parse_mode="HTML")

        elif switch_text == "суббота":
            timetable_message = ""

            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "1"
            else:
                current_week = "2"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT chat_id, user_group FROM user_table")
            result_set = cursor.fetchall()
            cursor.close()
            for i in result_set:
                if i[0] == message.from_user.id:
                    group = i[1]
            url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
            response = requests.get(url).json()
            adding = []
            for item in response["timetable"]:
                if item["week"] == current_week:
                    adding.append(
                        [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
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
                timetable_message += 'В субботу у этой группы пар нет!'
            await message.reply(timetable_message, parse_mode="HTML")
        elif switch_text == 'посмотреть расписание на след. неделю':
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(ScheduleUser.all()[3])
            await message.reply('Выберите день недели 👇\n(Вы будете смотреть следующую неделю)'
                                , reply=False, reply_markup=KeyBoards.day_of_the_week_kb2)
        else:
            await bot.send_message(message.from_user.id, messages.what)


@dp.message_handler(state=ScheduleUser.SCHEDULE_USER_3)
async def schedule_1(message: types.Message):
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        if switch_text == 'понедельник':
            timetable_message = ""
            current_week = "0"
            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "2"
            else:
                current_week = "1"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT user_group FROM user_table WHERE chat_id = '{message.from_user.id}'")
            result_set1 = cursor.fetchall()
            conn.commit()
            conn.close()
            url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
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
                timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Понедельник</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                for i in adding:
                    if i[0] == '1':
                        if i[4] == '' and i[5] == '':
                            timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                        else:
                            timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
            else:
                timetable_message += 'В следующий понедельник у этой группы пар нет!'
            await message.reply(timetable_message, parse_mode="HTML")

        elif switch_text == 'вторник':
            timetable_message = ""
            current_week = "0"
            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "2"
            else:
                current_week = "1"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT user_group FROM user_table WHERE chat_id = '{message.from_user.id}'")
            result_set1 = cursor.fetchall()
            conn.commit()
            conn.close()
            url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
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
                timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Вторник</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                for i in adding:
                    if i[0] == '2':
                        if i[4] == '' and i[5] == '':
                            timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                        else:
                            timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
            else:
                timetable_message += 'Во следующий вторник у этой группы пар нет!'
            await message.reply(timetable_message, parse_mode="HTML")

        elif switch_text == 'среда':
            timetable_message = ""
            current_week = "0"
            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "2"
            else:
                current_week = "1"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT user_group FROM user_table WHERE chat_id = '{message.from_user.id}'")
            result_set1 = cursor.fetchall()
            conn.commit()
            conn.close()
            url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
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
                timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Среда</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                for i in adding:
                    if i[0] == '3':
                        if i[4] == '' and i[5] == '':
                            timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                        else:
                            timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
            else:
                timetable_message += 'В следующую среду у этой группы пар нет!'
            await message.reply(timetable_message, parse_mode="HTML")

        elif switch_text == 'четверг':
            timetable_message = ""
            current_week = "0"
            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "2"
            else:
                current_week = "1"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT user_group FROM user_table WHERE chat_id = '{message.from_user.id}'")
            result_set1 = cursor.fetchall()
            conn.commit()
            conn.close()
            url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
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
                timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Четверг</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                for i in adding:
                    if i[0] == '4':
                        if i[4] == '' and i[5] == '':
                            timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                        else:
                            timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
            else:
                timetable_message += 'В следующий четверг у этой группы пар нет!'
            await message.reply(timetable_message, parse_mode="HTML")

        elif switch_text == 'пятница':
            timetable_message = ""
            current_week = "0"
            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "2"
            else:
                current_week = "1"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT user_group FROM user_table WHERE chat_id = '{message.from_user.id}'")
            result_set1 = cursor.fetchall()
            conn.commit()
            conn.close()
            url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
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
                timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Пятница</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                for i in adding:
                    if i[0] == '5':
                        if i[4] == '' and i[5] == '':
                            timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                        else:
                            timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
            else:
                timetable_message += 'В следующую пятницу у этой группы пар нет!'
            await message.reply(timetable_message, parse_mode="HTML")

        elif switch_text == 'суббота':
            timetable_message = ""
            current_week = "0"
            url = 'https://edu.sfu-kras.ru/timetable'
            response = requests.get(url).text
            match = re.search(r'Идёт\s\w{8}\sнеделя', response)
            if match:
                current_week = "2"
            else:
                current_week = "1"
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT user_group FROM user_table WHERE chat_id = '{message.from_user.id}'")
            result_set1 = cursor.fetchall()
            conn.commit()
            conn.close()
            url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
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
                timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Суббота</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                for i in adding:
                    if i[0] == '6':
                        if i[4] == '' and i[5] == '':
                            timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                        else:
                            timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
            else:
                timetable_message += 'В следующую субботу у этой группы пар нет!'
            await message.reply(timetable_message, parse_mode="HTML")
        elif switch_text == 'посмотреть расписание нынешней недели':
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(ScheduleUser.all()[2])
            await message.reply('Выберите день недели 👇\n(Вы будете смотреть нынешнюю неделю)'
                                , reply=False, reply_markup=KeyBoards.day_of_the_week_kb)
        else:
            await bot.send_message(message.from_user.id, messages.what)


# endregion

@dp.message_handler(state=Schedule.SCHEDULE_0)
async def schedule(message: types.Message):
    global group
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT is_teacher FROM users WHERE chat_id = '{message.from_user.id}'")
        teacher = cursor.fetchall()[0][0]
        if not teacher:
            if switch_text == 'понедельник':
                timetable_message = ""
                current_week = "0"
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_group FROM users WHERE chat_id = '{message.from_user.id}'")
                result_set1 = cursor.fetchall()
                conn.commit()
                conn.close()
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
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
                    timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Понедельник</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                    for i in adding:
                        if i[0] == '1':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'В следующий понедельник пар нет! Отличный повод увидеться с друзьями! 🎉'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == 'вторник':
                timetable_message = ""
                current_week = "0"
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_group FROM users WHERE chat_id = '{message.from_user.id}'")
                result_set1 = cursor.fetchall()
                conn.commit()
                conn.close()
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
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
                    timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Вторник</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                    for i in adding:
                        if i[0] == '2':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'Во следующий вторник пар нет! Отличный повод увидеться с друзьями! 🎉'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == 'среда':
                timetable_message = ""
                current_week = "0"
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_group FROM users WHERE chat_id = '{message.from_user.id}'")
                result_set1 = cursor.fetchall()
                conn.commit()
                conn.close()
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
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
                    timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Среда</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                    for i in adding:
                        if i[0] == '3':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'В следующую среду пар нет! Отличный повод увидеться с друзьями! 🎉'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == 'четверг':
                timetable_message = ""
                current_week = "0"
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_group FROM users WHERE chat_id = '{message.from_user.id}'")
                result_set1 = cursor.fetchall()
                conn.commit()
                conn.close()
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
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
                    timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Четверг</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                    for i in adding:
                        if i[0] == '4':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'В следующий четверг пар нет! Отличный повод увидеться с друзьями! 🎉'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == 'пятница':
                timetable_message = ""
                current_week = "0"
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_group FROM users WHERE chat_id = '{message.from_user.id}'")
                result_set1 = cursor.fetchall()
                conn.commit()
                conn.close()
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
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
                    timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Пятница</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                    for i in adding:
                        if i[0] == '5':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'В следующую пятницу пар нет! Отличный повод увидеться с друзьями! 🎉'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == 'суббота':
                timetable_message = ""
                current_week = "0"
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_group FROM users WHERE chat_id = '{message.from_user.id}'")
                result_set1 = cursor.fetchall()
                conn.commit()
                conn.close()
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
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
                    timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Суббота</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                    for i in adding:
                        if i[0] == '6':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'В следующую субботу пар нет! Отличный повод увидеться с друзьями! 🎉'
                await message.reply(timetable_message, parse_mode="HTML")
            elif switch_text == 'посмотреть расписание нынешней недели':
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(CheckSchedule.all()[0])
                await message.reply('Выберите день недели 👇\n(Вы будете смотреть нынешнюю неделю)'
                                    , reply=False, reply_markup=KeyBoards.day_of_the_week_kb)

            else:
                await bot.send_message(message.from_user.id, messages.what)
        else:
            if switch_text == 'понедельник':
                timetable_message = ""
                current_week = "0"
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_group FROM users WHERE chat_id = '{message.from_user.id}'")
                result_set1 = cursor.fetchall()
                conn.commit()
                conn.close()
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
                response = requests.get(url).json()
                adding = []
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
                flag = 0
                for i in adding:
                    if i[0] == '1':
                        if i[2] != '':
                            flag = 1
                if flag == 1:
                    timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Понедельник</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                    for i in adding:
                        if i[0] == '1':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'В следующий понедельник у вас пар нет!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == 'вторник':
                timetable_message = ""
                current_week = "0"
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_group FROM users WHERE chat_id = '{message.from_user.id}'")
                result_set1 = cursor.fetchall()
                conn.commit()
                conn.close()
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
                response = requests.get(url).json()
                adding = []
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
                flag = 0
                for i in adding:
                    if i[0] == '2':
                        if i[2] != '':
                            flag = 1
                if flag == 1:
                    timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Вторник</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                    for i in adding:
                        if i[0] == '2':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'Во следующий вторник у вас пар нет!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == 'среда':
                timetable_message = ""
                current_week = "0"
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_group FROM users WHERE chat_id = '{message.from_user.id}'")
                result_set1 = cursor.fetchall()
                conn.commit()
                conn.close()
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
                response = requests.get(url).json()
                adding = []
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
                flag = 0
                for i in adding:
                    if i[0] == '3':
                        if i[2] != '':
                            flag = 1
                if flag == 1:
                    timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Среда</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                    for i in adding:
                        if i[0] == '3':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'В следующую среду у вас пар нет!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == 'четверг':
                timetable_message = ""
                current_week = "0"
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_group FROM users WHERE chat_id = '{message.from_user.id}'")
                result_set1 = cursor.fetchall()
                conn.commit()
                conn.close()
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
                response = requests.get(url).json()
                adding = []
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
                flag = 0
                for i in adding:
                    if i[0] == '4':
                        if i[2] != '':
                            flag = 1
                if flag == 1:
                    timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Четверг</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                    for i in adding:
                        if i[0] == '4':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'В следующий четверг у вас пар нет!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == 'пятница':
                timetable_message = ""
                current_week = "0"
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_group FROM users WHERE chat_id = '{message.from_user.id}'")
                result_set1 = cursor.fetchall()
                conn.commit()
                conn.close()
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
                response = requests.get(url).json()
                adding = []
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
                flag = 0
                for i in adding:
                    if i[0] == '5':
                        if i[2] != '':
                            flag = 1
                if flag == 1:
                    timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Пятница</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                    for i in adding:
                        if i[0] == '5':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'В следующую пятницу у вас пар нет!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == 'суббота':
                timetable_message = ""
                current_week = "0"
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_group FROM users WHERE chat_id = '{message.from_user.id}'")
                result_set1 = cursor.fetchall()
                conn.commit()
                conn.close()
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set1[0][0]}')
                response = requests.get(url).json()
                adding = []
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
                flag = 0
                for i in adding:
                    if i[0] == '6':
                        if i[2] != '':
                            flag = 1
                if flag == 1:
                    timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Суббота</b>\n\t\t~~~~~~~~~~~~~~~~~~~'
                    for i in adding:
                        if i[0] == '6':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{i[2]} ({i[3]}) \n{i[4]}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'В следующую субботу у вас пар нет!'
                await message.reply(timetable_message, parse_mode="HTML")
            elif switch_text == 'посмотреть расписание нынешней недели':
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(CheckSchedule.all()[0])
                await message.reply('Выберите день недели 👇\n(Вы будете смотреть нынешнюю неделю)'
                                , reply=False, reply_markup=KeyBoards.day_of_the_week_kb)
            else:
                await bot.send_message(message.from_user.id, messages.what)


@dp.message_handler(state=CheckSchedule.SCH_0)
async def schedule_check(msg: types.Message):
    global group
    if msg.text.lower() == "меню":
        await msg.reply(messages.menu
                        , reply=False, reply_markup=KeyBoards.menu_admin_kb)
        state = dp.current_state(user=msg.from_user.id)
        await state.reset_state()
    else:
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT is_teacher FROM users WHERE chat_id = '{msg.from_user.id}'")
        teacher = cursor.fetchall()[0][0]
        switch_text = msg.text.lower()
        if not teacher:
            if switch_text == "понедельник":
                timetable_message = ""
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
                cursor.close()
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
                    timetable_message += 'В понедельник пар нет! Отличный повод увидеться с друзьями! 🎉'
                await msg.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "вторник":
                timetable_message = ""

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
                cursor.close()
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
                    timetable_message += 'Во вторник пар нет! Отличный повод увидеться с друзьями! 🎉'
                await msg.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "среда":
                timetable_message = ""

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
                cursor.close()
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
                    timetable_message += 'В среду пар нет! Отличный повод увидеться с друзьями! 🎉'
                await msg.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "четверг":
                timetable_message = ""

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
                cursor.close()
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
                    timetable_message += 'В четверг пар нет! Отличный повод увидеться с друзьями! 🎉'
                await msg.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "пятница":
                timetable_message = ""

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
                cursor.close()
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
                    timetable_message += 'В пятницу пар нет! Отличный повод увидеться с друзьями! 🎉'
                await msg.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "суббота":
                timetable_message = ""

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
                cursor.close()
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
                    timetable_message += 'В субботу пар нет! Отличный повод увидеться с друзьями! 🎉'
                await msg.reply(timetable_message, parse_mode="HTML")
            elif switch_text == 'посмотреть расписание на след. неделю':
                state = dp.current_state(user=msg.from_user.id)
                await state.set_state(Schedule.all()[0])
                await msg.reply('Выберите день недели 👇\n(Вы будете смотреть следующую неделю)'
                                , reply=False, reply_markup=KeyBoards.day_of_the_week_kb2)
            else:
                if msg.text != 'Посмотреть расписание на след. неделю':
                    await bot.send_message(msg.from_user.id, messages.what)
        else:
            if switch_text == "понедельник":
                timetable_message = ""
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
                cursor.close()
                for i in result_set:
                    if i[0] == msg.from_user.id:
                        group = i[1]
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
                response = requests.get(url).json()
                adding = []
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], "", item['type'], item['place']])
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
                    timetable_message += 'В понедельник у вас пар нет!'
                await msg.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "вторник":
                timetable_message = ""

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
                cursor.close()
                for i in result_set:
                    if i[0] == msg.from_user.id:
                        group = i[1]
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
                response = requests.get(url).json()
                adding = []
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
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
                    timetable_message += 'Во вторник у вас пар нет!'
                await msg.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "среда":
                timetable_message = ""

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
                cursor.close()
                for i in result_set:
                    if i[0] == msg.from_user.id:
                        group = i[1]
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
                response = requests.get(url).json()
                adding = []
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
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
                    timetable_message += 'В среду у вас пар нет!'
                await msg.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "четверг":
                timetable_message = ""

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
                cursor.close()
                for i in result_set:
                    if i[0] == msg.from_user.id:
                        group = i[1]
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
                response = requests.get(url).json()
                adding = []
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
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
                    timetable_message += 'В четверг у вас пар нет!'
                await msg.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "пятница":
                timetable_message = ""

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
                cursor.close()
                for i in result_set:
                    if i[0] == msg.from_user.id:
                        group = i[1]
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
                response = requests.get(url).json()
                adding = []
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
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
                    timetable_message += 'В пятницу у вас пар нет!'
                await msg.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "суббота":
                timetable_message = ""

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
                cursor.close()
                for i in result_set:
                    if i[0] == msg.from_user.id:
                        group = i[1]
                url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={group}')
                response = requests.get(url).json()
                adding = []
                for item in response["timetable"]:
                    if item["week"] == current_week:
                        adding.append(
                            [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
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
                    timetable_message += 'В субботу у вас пар нет!'
                await msg.reply(timetable_message, parse_mode="HTML")
            elif switch_text == 'посмотреть расписание на след. неделю':
                state = dp.current_state(user=msg.from_user.id)
                await state.set_state(Schedule.all()[0])
                await msg.reply('Выберите день недели 👇\n(Вы будете смотреть следующую неделю)'
                                , reply=False, reply_markup=KeyBoards.day_of_the_week_kb2)
            else:
                await bot.send_message(msg.from_user.id, messages.what)

        conn.close()


@dp.message_handler(state=Delete.DELETE_EVENTS_0)
async def schedule(message: types.Message):
    global group
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()

    elif switch_text == "добавить мероприятие":
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(Events.all()[0])
        await message.reply(messages.events_write, reply_markup=KeyBoards.universal_kb)

    else:
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(Delete.all()[3])
        incoming_events2[message.from_user.id] = message.text
        await message.reply(messages.events_del
                            , reply=False, reply_markup=KeyBoards.yes_or_no_keyboard2)


@dp.message_handler(state=Delete.DELETE_EVENTS_1)
async def schedule(message: types.Message):
    global group
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    else:
        state = dp.current_state(user=message.from_user.id)
        incoming_events2[message.from_user.id] = message.text
        await state.set_state(Delete.all()[2])
        await message.reply(messages.mailing_del
                            , reply=False, reply_markup=KeyBoards.yes_or_no_keyboard2)


@dp.message_handler(state=Delete.DELETE_EVENTS_2)
async def schedule(message: types.Message):
    global group
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    elif switch_text == 'да':
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(
            f"DELETE FROM `mail` WHERE (`chat_id` ==  {message.from_user.id} AND `event1` == '{incoming_events2[message.from_user.id]}');")
        incoming_events2.pop(message.from_user.id)
        conn.commit()
        conn.close()
        await bot.send_message(message.from_user.id, messages.successfully)
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()


@dp.message_handler(state=Delete.DELETE_EVENTS_3)
async def schedule(message: types.Message):
    global group
    switch_text = message.text.lower()
    if switch_text == 'меню':
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
    elif switch_text == 'да':
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(
            f"DELETE FROM `times` WHERE (`chat_id` ==  {message.from_user.id} AND `event1` == '{incoming_events2[message.from_user.id]}');")
        incoming_events2.pop(message.from_user.id)
        conn.commit()
        conn.close()
        await bot.send_message(message.from_user.id, messages.successfully)
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == message.from_user.id:
                is_succeed = True
        if is_succeed:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()
        else:
            await message.reply(messages.menu
                                , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.reset_state()


@dp.message_handler(state='*', content_types=["text"])
async def handler_message(msg: types.Message):
    global adding
    global group
    switch_text = msg.text.lower()
    if switch_text == "расписание":
        await dp.current_state(user=msg.from_user.id).set_state(CheckSchedule.all()[0])
        await msg.reply(messages.day_of_the_week, reply_markup=KeyBoards.day_of_the_week_kb)

    elif switch_text == "админ-панель":
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.execute(f"SELECT chat_id, is_teacher FROM users")
        result_set2 = cursor.fetchall()
        cursor.close()
        is_succeed = False
        is_teacher = False
        for item in result_set:
            if item[0] == msg.from_user.id:
                is_succeed = True
        for item in result_set2:
            if item[0] == msg.from_user.id:
                if item[1] == "True":
                    is_teacher = True
        if is_succeed:
            if is_teacher:
                state = dp.current_state(user=msg.from_user.id)
                await state.set_state(AdminPanel.all()[0])
                await msg.reply(messages.admin_panel, reply_markup=KeyBoards.admin_panel_teacher)
            else:
                state = dp.current_state(user=msg.from_user.id)
                await state.set_state(AdminPanel.all()[0])
                await msg.reply(messages.admin_panel, reply_markup=KeyBoards.admin_panel)
        else:
            await msg.reply(messages.not_admin, reply_markup=KeyBoards.menu_admin_kb)
    elif switch_text == "меню":
        is_succeed = False
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM admins")
        result_set = cursor.fetchall()
        cursor.close()
        for item in result_set:
            if item[0] == msg.from_user.id:
                is_succeed = True
        if is_succeed:
            await msg.reply(messages.menu
                            , reply=False, reply_markup=KeyBoards.menu_admin_kb)
            conn.commit()
            conn.close()
            state = dp.current_state(user=msg.from_user.id)
            await state.reset_state()
        else:
            await msg.reply(messages.menu
                            , reply=False, reply_markup=KeyBoards.menu_user_kb)
            conn.commit()
            conn.close()

    elif switch_text == "рассылки":
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM mail")
        result_set = cursor.fetchall()
        a = "Ваши рассылки: \n"
        for item in result_set:
            if item[0] == msg.from_user.id:
                local_time = time.ctime(item[2])
                local_time = local_time.split(' ')
                # день недели
                if local_time[0] == "Mon":
                    local_time[0] = "Понедельник"
                if local_time[0] == "Tue":
                    local_time[0] = "Вторник"
                if local_time[0] == "Wed":
                    local_time[0] = "Среда"
                if local_time[0] == "Thu":
                    local_time[0] = "Чеверг"
                if local_time[0] == "Fri":
                    local_time[0] = "Пятница"
                if local_time[0] == "Sat":
                    local_time[0] = "Суббота"
                if local_time[0] == "Sun":
                    local_time[0] = "Воскресенье"
                # месяц
                if local_time[1] == "Jan":
                    local_time[1] = "Января"
                if local_time[1] == "Feb":
                    local_time[1] = "Февраля"
                if local_time[1] == "Mar":
                    local_time[1] = "Марта"
                if local_time[1] == "Apr":
                    local_time[1] = "Апреля"
                if local_time[1] == "May":
                    local_time[1] = "Мая"
                if local_time[1] == "June":
                    local_time[1] = "Июня"
                if local_time[1] == "July":
                    local_time[1] = "Июля"
                if local_time[1] == "Aug":
                    local_time[1] = "Августа"
                if local_time[1] == "Sept":
                    local_time[1] = "Сентября"
                if local_time[1] == "Oct":
                    local_time[1] = "Октября"
                if local_time[1] == "Nov":
                    local_time[1] = "Ноября"
                if local_time[1] == "Dec":
                    local_time[1] = "Декабря"

                if local_time[2] == '':
                    a = a + f" - <b>{item[1]}</b>" + '\n' + \
                        f'Это рассылка заканчивается {local_time[3]} {local_time[1]} ' \
                        f'({local_time[0]}) {local_time[5]} года в {local_time[4]} ' + '\n'
                else:
                    a = a + f" - <b>{item[1]}</b>" + '\n' + \
                        f'Это рассылка заканчивается {local_time[2]} {local_time[1]} ' \
                        f'({local_time[0]}) {local_time[4]} года в {local_time[3]} ' + '\n'
        if a == "Ваши рассылки: \n":
            a = 'Вам еще не приходили рассылки!'
        await msg.reply(a, reply_markup=KeyBoards.mailing_lists_kb, parse_mode="HTML")

    elif switch_text == "профиль":
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, is_teacher FROM users")
        result_set = cursor.fetchall()
        is_teacher = False
        for item in result_set:
            if item[0] == msg.from_user.id:
                if item[1] == 'True':
                    is_teacher = True
        if is_teacher:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT chat_id, real_name FROM users")
            result_set = cursor.fetchall()
            for i in result_set:
                if i[0] == msg.from_user.id:
                    await bot.send_message(msg.from_user.id, f"Ваша фамилия: <b>{i[1]}</b>\n"
                                           , parse_mode="HTML")
            conn.commit()
            conn.close()
        else:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT chat_id, real_name, school, user_group FROM users")
            result_set = cursor.fetchall()
            for i in result_set:
                if i[0] == msg.from_user.id:
                    await bot.send_message(msg.from_user.id, f"Ваше имя: <b>{i[1]}</b>\n"
                                                             f"Ваш институт: <i><b>{i[2]}</b></i> 🎓\n"
                                                             f"Ваша группа: <i><b>{i[3]}</b></i> 🎓"
                                           , parse_mode="HTML")
            conn.commit()
            conn.close()
    elif switch_text == "настройки":
        await msg.reply(messages.settings, reply_markup=KeyBoards.setting_kb)

    elif switch_text == "запланированные мероприятия":
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM times")
        result_set = cursor.fetchall()
        a = "Ваши мероприятия: \n"
        for item in result_set:
            if item[0] == msg.from_user.id:
                local_time = time.ctime(item[2])
                local_time = local_time.split(' ')
                # день недели
                if local_time[0] == "Mon":
                    local_time[0] = "Понедельник"
                if local_time[0] == "Tue":
                    local_time[0] = "Вторник"
                if local_time[0] == "Wed":
                    local_time[0] = "Среда"
                if local_time[0] == "Thu":
                    local_time[0] = "Чеверг"
                if local_time[0] == "Fri":
                    local_time[0] = "Пятница"
                if local_time[0] == "Sat":
                    local_time[0] = "Суббота"
                if local_time[0] == "Sun":
                    local_time[0] = "Воскресенье"
                # месяц
                if local_time[1] == "Jan":
                    local_time[1] = "Января"
                if local_time[1] == "Feb":
                    local_time[1] = "Февраля"
                if local_time[1] == "Mar":
                    local_time[1] = "Марта"
                if local_time[1] == "Apr":
                    local_time[1] = "Апреля"
                if local_time[1] == "May":
                    local_time[1] = "Мая"
                if local_time[1] == "June":
                    local_time[1] = "Июня"
                if local_time[1] == "July":
                    local_time[1] = "Июля"
                if local_time[1] == "Aug":
                    local_time[1] = "Августа"
                if local_time[1] == "Sept":
                    local_time[1] = "Сентября"
                if local_time[1] == "Oct":
                    local_time[1] = "Октября"
                if local_time[1] == "Nov":
                    local_time[1] = "Ноября"
                if local_time[1] == "Dec":
                    local_time[1] = "Декабря"
                if local_time[2] == '':
                    a = a + f" - <b>{item[1]}</b>" + '\n' + \
                        f'Это мероприятие заканчивается {local_time[3]} {local_time[1]} ' \
                        f'({local_time[0]}) {local_time[5]} года в {local_time[4]} ' + '\n'
                else:
                    a = a + f" - <b>{item[1]}</b>" + '\n' + \
                        f'Это мероприятие заканчивается {local_time[2]} {local_time[1]} ' \
                        f'({local_time[0]}) {local_time[4]} года в {local_time[3]} ' + '\n'
        if a == "Ваши мероприятия: \n":
            a = 'У вас нет мероприятий!'
        await msg.reply(a, reply_markup=KeyBoards.events_kb, parse_mode="HTML")

    elif switch_text == "изменить информацию":
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, is_teacher FROM users")
        result_set = cursor.fetchall()
        is_teacher = False
        for item in result_set:
            if item[0] == msg.from_user.id:
                if item[1] == 'True':
                    is_teacher = True
        if is_teacher:
            await msg.reply(messages.choose_want_change, reply_markup=KeyBoards.change_information_kb2)
        else:
            await msg.reply(messages.choose_want_change, reply_markup=KeyBoards.change_information_kb)

    elif switch_text == "поменять преподавателя":
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(Register.all()[4])
        await msg.reply(messages.teacher_surname2)

    elif switch_text == "добавить мероприятие":
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(Events.all()[0])
        await msg.reply(messages.events_write, reply_markup=KeyBoards.universal_kb)

    elif switch_text == "удалить мероприятие":
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM times")
        result_set = cursor.fetchall()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for item in result_set:
            if item[0] == msg.from_user.id:
                keyboard.add(item[1])
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(Delete.all()[0])
        await msg.reply(messages.choose_event_del, reply_markup=keyboard)

    elif switch_text == "удалить рассылку":
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM mail")
        result_set = cursor.fetchall()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for item in result_set:
            if item[0] == msg.from_user.id:
                keyboard.add(item[1])
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(Delete.all()[1])
        await msg.reply(messages.choose_mail_del, reply_markup=keyboard)

    elif switch_text == "назад":
        await msg.reply(messages.settings, reply_markup=KeyBoards.setting_kb)

    # Изменение имени
    elif switch_text == "изменить имя":
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, real_name FROM users")
        result_set = cursor.fetchall()
        for i in result_set:
            if i[0] == msg.from_user.id:
                await bot.send_message(msg.from_user.id, f"Ваше прошлое имя: {i[1]}\n")
        conn.commit()
        conn.close()
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(Change.all()[0])
        await bot.send_message(msg.from_user.id, "Введите ваше имя 👇")

    # Изменение группы
    elif switch_text == "изменить группу":
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id, user_group, school FROM users")
        result_set = cursor.fetchall()
        for i in result_set:
            if i[0] == msg.from_user.id:
                await bot.send_message(msg.from_user.id,
                                       f"Ваш институт: <b>{i[2]}</b>\nВаша группа:"
                                       f" <b>{i[1]}</b>\n", parse_mode='HTML')
        conn.commit()
        conn.close()
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(Register.all()[2])
        await msg.reply(messages.choose_inst_change, reply_markup=KeyBoards.institute_kb)

    elif switch_text == "посмотреть расписание другой группы":
        await msg.reply(messages.choose_inst, reply_markup=KeyBoards.institute_kb)
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(ScheduleUser.all()[0])

    elif switch_text == "поддержка разработчиков":
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(Pay.all()[0])
        await msg.reply(messages.gratitude
                        , reply_markup=KeyBoards.developer_support_kb)
    elif switch_text == "test":
        await msg.reply(f"{messages.greets_msg}")
    else:
        await bot.send_message(msg.from_user.id, messages.what)


@dp.message_handler(commands='help')
async def process_start2_command(message: types.Message):
    if message.from_user.username != None:
        await message.reply(f'Welcome to StudentHelperBot, {message.from_user.username}!🔥\n'
                            '\n - Here you can always find the current schedule 🎓'
                            '\n - Set reminders 🍻'
                            '\n - Mailing lists from teachers ✉'
                            '\n - View the current schedule of another group ✌'
                            '\n - Support developers 👌'
                            '\n - We have our own PevCoin (currency in development) 💵'
                            '\n'
                            '\n  Registering? ✨'
                            '\n'
                            '\n ➖➖➖➖➖➖'
                            '\n'
                            '\n'
                            f'Добро пожаловать в StudentHelperBot, {message.from_user.username}!🔥\n'
                            '\n - Здесь всегда можно узнать актуальное расписание 🎓'
                            '\n - Поставить напоминания 🍻'
                            '\n - Рассылки от преподавателей ✉'
                            '\n - Посмотреть актуальное расписание другой группы ✌'
                            '\n - Поддержать разработчиков 👌'
                            '\n - У нас есть свои PevCoin\'ы (валюта в разработке) 💵'
                            '\n'
                            ' \n  Регистрируемся? ✨', reply_markup=KeyBoards.greet_kb)
    else:
        await message.reply(messages.greets_msg, reply_markup=KeyBoards.greet_kb)


if __name__ == "__main__":
    stopFlag = threading.Event()
    thread = MyThread(stopFlag)
    thread.start()
    stopFlag2 = threading.Event()
    thread2 = MyThread2(stopFlag2)
    thread2.start()
    executor.start_polling(dp, on_shutdown=shutdown, skip_updates=shutdown)

#  тестовый платеж убрать, визуализация, защита от sql инъекций
