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
from aiogram.types import ContentType, ReplyKeyboardMarkup, ParseMode
from aiogram.utils import executor
from aiogram.utils.markdown import text
from google_trans_new import google_translator

import KeyBoards
import messages
from config import TOKEN
from utils import Register, Change, AdminPanel, ScheduleUser, Events, Schedule, CheckSchedule, Delete, Change_Eu_Rus


# endregion


# region global
async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


translator = google_translator()
bot2 = telebot.TeleBot(__name__)
bot2.config['api_key'] = TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

incoming_events = {}
incoming_events2 = {}
incoming_event3 = {}
incoming_inst = []
incoming_inst2 = []


def only_letters(tested_string):
    for letter in tested_string:
        if letter not in KeyBoards.alphabet:
            return False
    return True


def translate(translate_text):
    translate_text = translator.translate(translate_text, lang_src='ru', lang_tgt='en')
    return translate_text


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
                    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{item[0]}'")
                    result_set = cursor.fetchall()
                    is_ru = False
                    if result_set[0][0] == "True":
                        is_ru = True
                    if is_ru == True:
                        cursor.execute(
                            f"UPDATE `times` SET `30min`= {0} WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                        bot2.send_message(item[0],
                                          f'{real_name[0][0]}! Мероприятие: {item[1]} состоится через пол часа')
                    else:
                        cursor.execute(
                            f"UPDATE `times` SET `30min`= {0} WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                        bot2.send_message(item[0],
                                          f'{real_name[0][0]}! Event: {item[1]} it will take place in half an hour')

            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `times` WHERE `time` <=  strftime('%s', 'now') + 300;")
            result_set5 = cursor.fetchall()
            for item in result_set5:
                cursor.execute(f"SELECT `real_name` FROM `users` WHERE `chat_id` = {item[0]}")
                real_name = cursor.fetchall()
                cursor.execute(f"SELECT `5min` FROM `times` WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                state = cursor.fetchall()
                if state[0][0] == 1:
                    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{item[0]}'")
                    result_set = cursor.fetchall()
                    is_ru = False
                    if result_set[0][0] == "True":
                        is_ru = True
                    if is_ru == True:
                        cursor.execute(
                            f"UPDATE `times` SET `5min`= {0} WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                        bot2.send_message(item[0],
                                          f'{real_name[0][0]}! Мероприятие: {item[1]} состоится через пять минут')
                    else:
                        cursor.execute(
                            f"UPDATE `times` SET `5min`= {0} WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                        bot2.send_message(item[0],
                                          f'{real_name[0][0]}! Event: {item[1]} it will take place in five minutes')

            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `times` WHERE `time` <=  strftime('%s', 'now');")
            result_set = cursor.fetchall()
            cursor.execute(f"DELETE FROM `times` WHERE `time` <=  strftime('%s', 'now');")
            conn.commit()
            for item in result_set:
                cursor.execute(f"SELECT `real_name` FROM `users` WHERE `chat_id` = {item[0]}")
                real_name = cursor.fetchall()
                cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{item[0]}'")
                result_set = cursor.fetchall()
                is_ru = False
                if result_set[0][0] == "True":
                    is_ru = True
                if is_ru == True:
                    bot2.send_message(item[0], f'{real_name[0][0]}! Ваше мероприятие: {item[1]}\nокончено')
                else:
                    bot2.send_message(item[0], f'{real_name[0][0]}! Your event: {item[1]}\nfinished')

            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `mail` WHERE `time` <=  strftime('%s', 'now') + 1800;")
            result_set30 = cursor.fetchall()
            for item in result_set30:
                cursor.execute(f"SELECT `real_name` FROM `users` WHERE `chat_id` = {item[0]}")
                real_name = cursor.fetchall()
                cursor.execute(f"SELECT `30min` FROM `mail` WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                state = cursor.fetchall()
                if state[0][0] == 1:
                    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{item[0]}'")
                    result_set = cursor.fetchall()
                    is_ru = False
                    if result_set[0][0] == "True":
                        is_ru = True
                    if is_ru == True:
                        cursor.execute(
                            f"UPDATE `mail` SET `30min`= {0} WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                        bot2.send_message(item[0], f'{real_name[0][0]}! Рассылка: {item[1]} состоится через пол часа')
                    else:
                        cursor.execute(
                            f"UPDATE `mail` SET `30min`= {0} WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                        bot2.send_message(item[0],
                                          f'{real_name[0][0]}! Mailing: {item[1]} it will take place in half an hour')

            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM `mail` WHERE `time` <=  strftime('%s', 'now') + 300;")
            result_set5 = cursor.fetchall()
            for item in result_set5:
                cursor.execute(f"SELECT `real_name` FROM `users` WHERE `chat_id` = {item[0]}")
                real_name = cursor.fetchall()
                cursor.execute(f"SELECT `5min` FROM `mail` WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                state = cursor.fetchall()
                if state[0][0] == 1:
                    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{item[0]}'")
                    result_set = cursor.fetchall()
                    is_ru = False
                    if result_set[0][0] == "True":
                        is_ru = True
                    if is_ru == True:
                        cursor.execute(
                            f"UPDATE `mail` SET `5min`= {0} WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                        bot2.send_message(item[0], f'{real_name[0][0]}! Рассылка: {item[1]} состоится через пять минут')
                    else:
                        cursor.execute(
                            f"UPDATE `mail` SET `5min`= {0} WHERE (`chat_id` = {item[0]} AND `event1` = '{item[1]}');")
                        bot2.send_message(item[0],
                                          f'{real_name[0][0]}! Mailing: {item[1]} it will take place in five minutes')

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
                cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{item[0]}'")
                result_set = cursor.fetchall()
                is_ru = False
                if result_set[0][0] == "True":
                    is_ru = True
                if is_ru == True:
                    bot2.send_message(item[0], f'{real_name[0][0]}! Рассылка: {item[1]} закончилась')
                else:
                    bot2.send_message(item[0], f'{real_name[0][0]}! Mailing: {item[1]} ended')
                conn.commit()
                conn.close()


class MyThread2(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global adding
        while not self.stopped.wait(50):
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
                        date_kur = a[0].split(':')
                        listing_date = []
                        for n in date_kur:
                            n = int(n)
                            listing_date.append(n)
                        listing_date_sum2 = listing_date[0] * 60 - 7 * 60 + listing_date[1]
                        if listing_date_sum == listing_date_sum2:
                            conn = sqlite3.connect('db.db')
                            cursor = conn.cursor()
                            cursor.execute(f"SELECT chat_id, real_name FROM users WHERE user_group = '{i[0]}'")
                            id_group = cursor.fetchall()
                            cursor.close()
                            for k in id_group:
                                if j[5] == "":
                                    conn = sqlite3.connect('db.db')
                                    cursor = conn.cursor()
                                    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{k[0]}'")
                                    result_set = cursor.fetchall()
                                    is_ru = False
                                    if result_set[0][0] == "True":
                                        is_ru = True
                                    if is_ru == True:
                                        bot2.send_message(k[0], f'{k[1]}, у вас начинается {j[2]}')
                                    else:
                                        bot2.send_message(k[0], f"{k[1]}, you starting to {translate(j[2])}")
                                else:
                                    conn = sqlite3.connect('db.db')
                                    cursor = conn.cursor()
                                    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{k[0]}'")
                                    result_set = cursor.fetchall()
                                    is_ru = False
                                    if result_set[0][0] == "True":
                                        is_ru = True
                                    if is_ru == True:
                                        bot2.send_message(k[0], f'{k[1]}, у вас начинается {j[2]} в {j[5]}')
                                    else:
                                        bot2.send_message(k[0], f"{k[1]}, you starting to {translate(j[2])} in {j[5]}")
                        if listing_date_sum == listing_date_sum2 - 5:
                            conn = sqlite3.connect('db.db')
                            cursor = conn.cursor()
                            cursor.execute(f"SELECT chat_id, real_name FROM users WHERE user_group = '{i[0]}'")
                            id_group = cursor.fetchall()
                            cursor.close()
                            for k in id_group:
                                if j[5] == "":
                                    conn = sqlite3.connect('db.db')
                                    cursor = conn.cursor()
                                    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{k[0]}'")
                                    result_set = cursor.fetchall()
                                    is_ru = False
                                    if result_set[0][0] == "True":
                                        is_ru = True
                                    if is_ru == True:
                                        bot2.send_message(k[0], f'{k[1]}, у вас через 5 минут начнется {j[2]}')
                                    else:
                                        bot2.send_message(k[0],
                                                          f'{k[1]}, you will start in 5 minutes {translate(j[2])}')
                                else:
                                    conn = sqlite3.connect('db.db')
                                    cursor = conn.cursor()
                                    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{k[0]}'")
                                    result_set = cursor.fetchall()
                                    is_ru = False
                                    if result_set[0][0] == "True":
                                        is_ru = True
                                    if is_ru == True:
                                        bot2.send_message(k[0], f'{k[1]}, у вас начнется {j[2]} через 5 минут в {j[5]}')
                                    else:
                                        bot2.send_message(k[0],
                                                          f'{k[1]}, you will start {translate(j[2])} after 5 minutes in the {j[5]}')


class MyThread3(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global adding2, a, data, mes
        while not self.stopped.wait(60):
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT chat_id FROM users")
            result_set2 = cursor.fetchall()
            cursor.close()
            date = datetime.datetime.today()
            date_date = date.strftime('%H:%M')
            date_split = date_date.split(':')
            listing_date_split = []
            for n in date_split:
                n = int(n)
                listing_date_split.append(n)
            listing_date_sum = listing_date_split[0] * 60 + listing_date_split[1]
            if listing_date_sum == 0:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE `users` SET `7utra` = '{1}'")
                conn.commit()
                conn.close()
            for l in result_set2:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT `7utra` FROM users WHERE chat_id = '{l[0]}'")
                result_set2 = cursor.fetchall()
                cursor.close()
                if result_set2[0][0] == 1:
                    conn = sqlite3.connect('db.db')
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE `users` SET `7utra` = '{0}' WHERE `chat_id` = '{l[0]}'")
                    conn.commit()
                    conn.close()
                    conn = sqlite3.connect('db.db')
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT `user_group` FROM users WHERE chat_id = '{l[0]}'")
                    result_set2 = cursor.fetchall()
                    cursor.close()
                    url = 'https://edu.sfu-kras.ru/timetable'
                    response = requests.get(url).text
                    match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                    if match:
                        current_week = "1"
                    else:
                        current_week = "2"
                    url = f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set2[0][0]}'
                    response = requests.get(url).json()
                    adding2 = []
                    for item in response["timetable"]:
                        if item["week"] == current_week:
                            adding2.append(
                                [item['day'], item['time'], item['subject'], item['type'], "", item['place']])
                    date = datetime.datetime.today()
                    date_date = date.strftime('%H:%M')
                    date_split = date_date.split(':')
                    listing_date_split = []
                    for n in date_split:
                        n = int(n)
                        listing_date_split.append(n)
                    local_time_now = time.time()
                    local_time = time.ctime(local_time_now)
                    local_time = local_time.split(' ')
                    a = '0'
                    if local_time[0] == "Mon":
                        a = '1'
                        local_time[0] = "понедельник"
                    if local_time[0] == "Tue":
                        a = '2'
                        local_time[0] = "вторник"
                    if local_time[0] == "Wed":
                        a = '3'
                        local_time[0] = "среда"
                    if local_time[0] == "Thu":
                        a = '4'
                        local_time[0] = "четверг"
                    if local_time[0] == "Fri":
                        a = '5'
                        local_time[0] = "пятница"
                    if local_time[0] == "Sat":
                        a = '6'
                        local_time[0] = "суббота"
                    if local_time[0] == "Sun":
                        a = '7'
                        local_time[0] = "воскресенье"
                    s_city = "Красноярск,RU"
                    city_id = 0
                    appid = "8fb0b9a76ed0af2c84d8fae4a6f61133"
                    try:
                        res = requests.get("http://api.openweathermap.org/data/2.5/find?",
                                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
                        data = res.json()
                        city_id = data['list'][0]['id']
                    except Exception:
                        pass
                    try:
                        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
                        data = res.json()
                    except Exception:
                        pass
                    try:
                        listik = []
                        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
                        kaka = res.json()
                        for t in kaka['list']:
                            q = t['dt_txt'].split(" ")
                            if q[1] == '03:00:00':
                                q[1] = "03:00"
                            if q[1] == '21:00:00':
                                q[1] = "21:00"
                            if q[1] == '18:00:00':
                                q[1] = "18:00"
                            if q[1] == '15:00:00':
                                q[1] = "15:00"
                            if q[1] == '12:00:00':
                                q[1] = "12:00"
                            if q[1] == '9:00:00':
                                q[1] = "09:00"
                            if q[1] == '09:00:00':
                                q[1] = "09:00"
                            if q[1] == '06:00:00':
                                q[1] = "06:00"
                            if q[1] == '6:00:00':
                                q[1] = "06:00"

                            listik.append(q[1])
                            listik.append('{0:+3.0f}°'.format(t['main']['temp']))
                            listik.append(t['weather'][0]['description'])
                            if q[1] == "15:00":
                                break
                        conn = sqlite3.connect('db.db')
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{l[0]}'")
                        result_set = cursor.fetchall()
                        is_ru = False
                        if result_set[0][0] == "True":
                            is_ru = True
                        if is_ru == True:
                            mes = ''
                            j = 0
                            for s in listik:
                                if j == 0:
                                    mes += "В "
                                mes += s
                                j += 1
                                if j != 3:
                                    mes += ", "
                                if j == 3:
                                    mes += "\n"
                                    j = 0
                        else:
                            mes = ''
                            j = 0
                            for s in listik:
                                if j == 0:
                                    mes += "В "
                                mes += translate(s)
                                j += 1
                                if j != 3:
                                    mes += ", "
                                if j == 3:
                                    mes += "\n"
                                    j = 0
                    except Exception:
                        pass
                    conn = sqlite3.connect('db.db')
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT chat_id, real_name FROM users WHERE chat_id = '{l[0]}'")
                    id_group = cursor.fetchall()
                    cursor.close()
                    timetable_message = ""
                    url = 'https://edu.sfu-kras.ru/timetable'
                    response = requests.get(url).text
                    match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                    if match:
                        current_week = "1"
                    else:
                        current_week = "2"
                    url = (f'http://edu.sfu-kras.ru/api/timetable/get?target={result_set2[0][0]}')
                    response = requests.get(url).json()
                    adding = []
                    for item in response["timetable"]:
                        if item["week"] == current_week:
                            adding.append(
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for p in adding:
                        if p[0] == a:
                            if p[2] != '':
                                flag = 1
                    conn = sqlite3.connect('db.db')
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{l[0]}'")
                    result_set = cursor.fetchall()
                    is_ru = False
                    if result_set[0][0] == "True":
                        is_ru = True
                    if is_ru == False:
                        if flag == 1:
                            for u in adding:
                                if u[0] == a:
                                    if u[4] == '' and u[5] == '':
                                        timetable_message += f'\n{u[1]}\n{translate(u[2])} ({translate(u[3])})\n'
                                    else:
                                        timetable_message += f'\n{u[1]}\n{translate(u[2])} ({translate(u[3])}) \n{translate(u[4])}\n{u[5]}\n'
                    else:
                        if flag == 1:
                            for u in adding:
                                if u[0] == a:
                                    if u[4] == '' and u[5] == '':
                                        timetable_message += f'\n{u[1]}\n{u[2]} ({u[3]})\n'
                                    else:
                                        timetable_message += f'\n{u[1]}\n{u[2]} ({u[3]}) \n{u[4]}\n{u[5]}\n'
                    for k in id_group:
                        conn = sqlite3.connect('db.db')
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{k[0]}'")
                        result_set = cursor.fetchall()
                        is_ru = False
                        if result_set[0][0] == "True":
                            is_ru = True
                        if flag == 1:
                            if is_ru == True:
                                bot2.send_message(k[0], f"Доброе утро, {k[1]}!\n\nСегодня {local_time[0]}, "
                                                        f"сейчас {data['weather'][0]['description']}\n\nТемпература в Красноярске "
                                                        f"{round(int(data['main']['temp']))}°.\n\nПрогноз погоды на сегодня:\n\n{mes}\nУ вас сегодня\n{timetable_message}")
                            else:
                                bot2.send_message(k[0], f"Good morning, {k[1]}!\n\nToday {translate(local_time[0])}, "
                                                        f"now {translate(data['weather'][0]['description'])}\n\nTemperature in Krasnoyarsk "
                                                        f"{round(int(data['main']['temp']))}°.\n\nToday's weather forecast:\n\n{mes}\nYou have today\n{timetable_message}")
                        else:
                            if is_ru == True:
                                bot2.send_message(k[0], f"Доброе утро, {k[1]}!\n\nСегодня {local_time[0]}, "
                                                        f"сейчас {data['weather'][0]['description']}\n\nТемпература в Красноярске "
                                                        f"{round(int(data['main']['temp']))}°.\n\nПрогноз погоды на сегодня:\n\n{mes}\nУ вас сегодня пар нет! Отличный повод увидеться с друзьями! 🎉'")
                            else:
                                bot2.send_message(k[0], f"Good morning, {k[1]}!\n\nToday {translate(local_time[0])}, "
                                                        f"now {translate(data['weather'][0]['description'])}\n\nTemperature in Krasnoyarsk "
                                                        f"{round(int(data['main']['temp']))}°.\n\nToday's weather forecast:\n\n{mes}\nYou have today no couples, a great reason to see your friends! 🎉")

class MyThread4(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(3600):
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT ru FROM users WHERE chat_id = 1008740088")
            result_set = cursor.fetchall()
            bot2.send_message(1008740088, f"Язык на сервере {result_set[0][0]}")
# endregions

@dp.message_handler(state='*', commands='start')
async def process_start_command(message: types.Message):
    is_succeed = False
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users(chat_id, name) values ({message.from_user.id}, '{message.from_user.username}')")
    conn.commit()
    conn.close()
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT is_teacher FROM admins WHERE user_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    try:
        if result_set[0][0] == 'True' and result_set[0][0] != None:
            is_succeed = True
    except:
        pass
    if message.from_user.username != None:
        if is_succeed == True:
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
                                ' \n  Регистрируемся? ✨', reply_markup=KeyBoards.select_RU_EN)
        else:
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
                                ' \n  Регистрируемся? ✨', reply_markup=KeyBoards.select_RU_EN)
    else:
        if is_succeed == True:
            await message.reply(messages.greets_msg, reply_markup=KeyBoards.select_RU_EN)
        else:
            await message.reply(messages.greets_msg, reply_markup=KeyBoards.select_RU_EN)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(Register.all()[0])


# region userHandler
@dp.message_handler(state=Events.EVENTS_USER_0)
async def process_command0(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Events.all()[1])
                incoming_events[message.from_user.id] = message.text
                await message.reply(messages.events
                                    , reply_markup=KeyBoards.time_kb)
            else:
                await bot.send_message(message.from_user.id, messages.message_error9)
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()

        else:
            if only_letters(message.text) == True:
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Events.all()[1])
                incoming_events[message.from_user.id] = message.text
                await message.reply(messages.events_en
                                    , reply_markup=KeyBoards.time_kb_en)
            else:
                await bot.send_message(message.from_user.id, messages.message_error9_en)


@dp.message_handler(state=Events.EVENTS_USER_1)
async def process_command1(message: types.Message):
    global timing
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        else:
            m = {'1 hour': 60 * 60, "2 hours": 60 * 60 * 2, "3 hours": 60 * 60 * 3, "4 hours": 60 * 60 * 4,
                 "5 hours": 60 * 60 * 5,
                 "18 hours": 60 * 60 * 18, "6 hours": 60 * 60 * 6, "12 hours": 60 * 60 * 12,
                 "24 hours": 60 * 60 * 24,
                 "2 days": 60 * 60 * 48, "3 days": 60 * 60 * 24 * 3, "A week": 60 * 60 * 24 * 7}
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
                        await message.reply(messages.successfully_en
                                            , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                        conn.commit()
                        conn.close()
                        state = dp.current_state(user=message.from_user.id)
                        await state.reset_state()
                    else:
                        await message.reply(messages.successfully_en
                                            , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                        conn.commit()
                        conn.close()
                        state = dp.current_state(user=message.from_user.id)
                        await state.reset_state()
            except KeyError:
                await bot.send_message(message.from_user.id, messages.message_error4_en)


# endregion


# region adminHandler
@dp.message_handler(state=AdminPanel.ADMIN_0)
async def process_admin_command2(message: types.Message):
    switch_text = message.text.lower()
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
        elif switch_text == "добавить преподавателя":
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT real_name, chat_id FROM users")
            result_set = cursor.fetchall()
            cursor.close()
            keyboard = ReplyKeyboardMarkup().add("Меню")
            for item in result_set:
                a = str(item[0])+":"+str(item[1])
                keyboard.add(a)
            await message.reply(messages.select, reply_markup=keyboard)
            await dp.current_state(user=message.from_user.id).set_state(AdminPanel.all()[9])
        else:
            await bot.send_message(message.from_user.id, messages.what)
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        elif switch_text == "add a teacher":
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT real_name, chat_id FROM users")
            result_set = cursor.fetchall()
            cursor.close()
            keyboard = ReplyKeyboardMarkup().add("Menu")
            for item in result_set:
                a = str(item[0]) + ":" + str(item[1])
                keyboard.add(a)
            await message.reply(messages.select, reply_markup=keyboard)
            await dp.current_state(user=message.from_user.id).set_state(AdminPanel.all()[9])
        elif switch_text == 'send a newsletter':
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(AdminPanel.all()[1])
            await message.reply(messages.write_mail_en, reply_markup=KeyBoards.return_keyboard_en)
        elif switch_text == 'send a newsletter to all users':
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(AdminPanel.all()[6])
            await message.reply(messages.write_mail_en, reply_markup=KeyBoards.return_keyboard_en)
        else:
            await bot.send_message(message.from_user.id, messages.what_en)


@dp.message_handler(state=AdminPanel.ADMIN_1)
async def process_admin_command1(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
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
                await message.reply(messages.university_en, reply_markup=KeyBoards.institute_kb)
            else:
                await bot.send_message(message.from_user.id, messages.message_error5_en)


@dp.message_handler(state=AdminPanel.ADMIN_2)
async def process_admin_command4(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
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
                        await message.reply(messages.group_message_en, reply_markup=keyboard)
                        state = dp.current_state(user=message.from_user.id)
                        await state.set_state(AdminPanel.all()[3])
                    else:
                        await bot.send_message(message.from_user.id, messages.message_error_en)
            except KeyError:
                await bot.send_message(message.from_user.id, messages.message_error_en)


@dp.message_handler(state=AdminPanel.ADMIN_3)
async def process_admin_command4(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
                        f"UPDATE admins SET `group` = '{message.text}' WHERE user_id = '{message.from_user.id}'")
                    conn.commit()
                    conn.close()
                    state = dp.current_state(user=message.from_user.id)
                    await state.set_state(AdminPanel.all()[4])
                    await message.reply(messages.timer, reply=False, reply_markup=KeyBoards.time_kb2)
                else:
                    await bot.send_message(message.from_user.id, messages.message_error6)
            else:
                await bot.send_message(message.from_user.id, messages.message_error6)
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
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
                        f"UPDATE admins SET `group` = '{message.text}' WHERE user_id = '{message.from_user.id}'")
                    conn.commit()
                    conn.close()
                    state = dp.current_state(user=message.from_user.id)
                    await state.set_state(AdminPanel.all()[4])
                    await message.reply(messages.timer_en, reply=False, reply_markup=KeyBoards.time_kb2_en)
                else:
                    await bot.send_message(message.from_user.id, messages.message_error6_en)
            else:
                await bot.send_message(message.from_user.id, messages.message_error6_en)


@dp.message_handler(state=AdminPanel.ADMIN_4)
async def process_admin_command4(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
            m = {'Без таймера': 10, '1 час': 60 * 60, "2 часа": 60 * 60 * 2, "3 часа": 60 * 60 * 3,
                 "4 часа": 60 * 60 * 4,
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
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        else:
            m = {'Without a timer': 10, '1 hour': 60 * 60, "2 hours": 60 * 60 * 2, "3 hours": 60 * 60 * 3,
                 "4 hours": 60 * 60 * 4,
                 "5 hours": 60 * 60 * 5,
                 "18 hours": 60 * 60 * 18, "6 hours": 60 * 60 * 6, "12 hours": 60 * 60 * 12,
                 "24 hours": 60 * 60 * 24,
                 "2 days": 60 * 60 * 48, "3 days": 60 * 60 * 24 * 3, "A week": 60 * 60 * 24 * 7}
            try:
                if m[message.text]:
                    conn = sqlite3.connect('db.db')
                    cursor = conn.cursor()
                    if message.text != 'Without a timer':
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
                    await message.reply(messages.mailing_en, reply=False, reply_markup=KeyBoards.
                                        yes_or_no_keyboard_en)
            except KeyError:
                await bot.send_message(message.from_user.id, messages.message_error4_en)


@dp.message_handler(state=AdminPanel.ADMIN_5)
async def process_admin_command1(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
                cursor.execute(f"SELECT `ru` FROM users WHERE chat_id = '{user[0]}'")
                rus = cursor.fetchall()
                cursor.close()
                if group_users == group:
                    if rus[0][0] == 1:
                        a = f'Рассылка от пользователя: <b>{name[0][0]}</b>\n' + '\n ➖➖➖➖➖➖ \n\n' + f'<i>{content[0][0]}</i>'
                    else:
                        a = f'Mailing list from the user: <b>{name[0][0]}</b>\n' +'\n ➖➖➖➖➖➖ \n\n' + f'<i>{translate(content[0][0])}</i>'
                    if incoming_event3[message.from_user.id] == 'Без таймера':
                        pass
                    else:
                        conn = sqlite3.connect('db.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            f"INSERT INTO mail(`chat_id`, `event1`, `time`, `30min`, `5min`) values ({user[0]}, '{content[0][0]}', {time2[0][0]}, {1}, {1})")
                        conn.commit()
                        conn.close()
                    try:
                        await bot.send_message(user[0], a, parse_mode='HTML')
                    except:
                        pass
            incoming_event3.pop(message.from_user.id)
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
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        elif switch_text == 'yes':
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
                cursor.execute(f"SELECT `ru` FROM users WHERE chat_id = '{user[0]}'")
                rus = cursor.fetchall()
                cursor.close()
                if group_users == group:
                    if rus[0][0] == 1:
                        a = f'Рассылка от пользователя: <b>{name[0][0]}</b>\n' + '\n ➖➖➖➖➖➖ \n\n' + f'<i>{content[0][0]}</i>'
                    else:
                        a = f'Mailing list from the user: <b>{name[0][0]}</b>\n' + '\n ➖➖➖➖➖➖ \n\n' + f'<i>{translate(content[0][0])}</i>'
                    if incoming_event3[message.from_user.id] == 'Without a timer':
                        try:
                            await bot.send_message(user[0], a, parse_mode='HTML')
                        except:
                            pass
                    else:

                        conn = sqlite3.connect('db.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            f"INSERT INTO mail(`chat_id`, `event1`, `time`, `30min`, `5min`) values ({user[0]}, '{content[0][0]}', {time2[0][0]}, {1}, {1})")
                        try:
                            await bot.send_message(user[0], a, parse_mode='HTML')
                        except:
                            pass
                        conn.commit()
                        conn.close()

            incoming_event3.pop(message.from_user.id)
            await dp.bot.send_message(message.from_user.id,
                                      f'Your newsletter: <b>{content[0][0]}</b>\nSuccessfully sent to the group '
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
                await message.reply(messages.successfully_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.successfully_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()

        elif switch_text == 'to change':
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(AdminPanel.all()[0])
            await message.reply("Select an action ✨", reply_markup=KeyBoards.admin_panel_en)


@dp.message_handler(state=AdminPanel.ADMIN_6)
async def process_admin_command1(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
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
                await message.reply(messages.timer_en, reply_markup=KeyBoards.time_kb2_en)
            else:
                await bot.send_message(message.from_user.id, messages.message_error5_en)


@dp.message_handler(state=AdminPanel.ADMIN_7)
async def process_admin_command4(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
            m = {'Без таймера': 10, '1 час': 60 * 60, "2 часа": 60 * 60 * 2, "3 часа": 60 * 60 * 3,
                 "4 часа": 60 * 60 * 4,
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
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        else:
            m = {'Without a timer': 10, '1 hour': 60 * 60, "2 hours": 60 * 60 * 2, "3 hours": 60 * 60 * 3,
                 "4 hours": 60 * 60 * 4,
                 "5 hours": 60 * 60 * 5,
                 "18 hours": 60 * 60 * 18, "6 hours": 60 * 60 * 6, "12 hours": 60 * 60 * 12,
                 "24 hours": 60 * 60 * 24,
                 "2 days": 60 * 60 * 48, "3 days": 60 * 60 * 24 * 3, "A week": 60 * 60 * 24 * 7}
            try:
                if m[message.text]:
                    conn = sqlite3.connect('db.db')
                    cursor = conn.cursor()
                    if message.text != 'Without a timer':
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
                    await message.reply(messages.mailing_en, reply=False, reply_markup=KeyBoards.
                                        yes_or_no_keyboard_en)
            except KeyError:
                await bot.send_message(message.from_user.id, messages.message_error4_en)


@dp.message_handler(state=AdminPanel.ADMIN_8)
async def process_admin_command1(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
                    conn = sqlite3.connect('db.db')
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT `ru` FROM users WHERE chat_id = '{message.from_user.id}'")
                    rus = cursor.fetchall()
                    cursor.close()
                    if rus[0][0]:
                        a = f'Рассылка от пользователя: <b>{name[0][0]}</b>\n' + '\n ➖➖➖➖➖➖ \n\n' + f'<i>{content[0][0]}</i>'
                    else:
                        a = f'Mailing list from the user: <b>{name[0][0]}</b>\n' + '\n ➖➖➖➖➖➖ \n\n' + f'<i>{translate(content[0][0])}</i>'
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
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        elif switch_text == 'yes':
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
                    conn = sqlite3.connect('db.db')
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT `ru` FROM users WHERE chat_id = '{message.from_user.id}'")
                    rus = cursor.fetchall()
                    cursor.close()
                    if rus[0][0]:
                        a = f'Рассылка от пользователя: <b>{name[0][0]}</b>\n' + '\n ➖➖➖➖➖➖ \n\n' + f'<i>{content[0][0]}</i>'
                    else:
                        a = f'Mailing list from the user: <b>{name[0][0]}</b>\n' + '\n ➖➖➖➖➖➖ \n\n' + f'<i>{translate(content[0][0])}</i>'
                    if incoming_event3[message.from_user.id] != 'Without a timer':
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
                                      f'Your newsletter: <b>{content[0][0]}</b>\nSuccessfully sent to everyone!'
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
                await message.reply(messages.successfully_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.successfully_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()

        elif switch_text == 'to change':
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(AdminPanel.all()[0])
            await message.reply(messages.choose_action_en, reply_markup=KeyBoards.admin_panel_en)


@dp.message_handler(state=AdminPanel.ADMIN_9)
async def process_admin_command1(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
                k = message.text
                a = k.split(":")
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_id FROM admins WHERE user_id = '{a[1]}'")
                result_set2 = cursor.fetchall()
                if result_set2 == []:
                    await bot.send_message(a[1], f"Здравствуйте, <b>{a[0]}</b>, вас добавили в список преподавателей.\n"
                                             f"Нажмите на /start и <b>зарегистрируйтесь</b> за преподавателя.", parse_mode= "HTML")
                    cursor.execute(
                        f"INSERT INTO admins(user_id, is_teacher, name_admin) values ({a[1]}, '{True}', '{a[0]}')")
                    conn.commit()
                    conn.close()
                    await bot.send_message(message.from_user.id, messages.successfully)
                else:
                    await bot.send_message(message.from_user.id, "Пользователь уже преподаватель!")
            except:
                await bot.send_message(message.from_user.id, "Пользователь заблокировал бота")
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
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        else:
            try:
                k = message.text
                a = k.split(":")
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT user_id FROM admins WHERE user_id = '{a[1]}'")
                result_set2 = cursor.fetchall()
                if result_set2 == []:
                    await bot.send_message(a[1], f"Здравствуйте, <b>{a[0]}</b>, вас добавили в список преподавателей.\n"
                                                 f"Нажмите на /start и <b>зарегистрируйтесь</b> за преподавателя.",
                                           parse_mode="HTML")
                    cursor.execute(
                        f"INSERT INTO admins(user_id, is_teacher, name_admin) values ({a[1]}, '{True}', '{a[0]}')")
                    conn.commit()
                    conn.close()
                    await bot.send_message(message.from_user.id, messages.successfully_en)
                else:
                    await bot.send_message(message.from_user.id, "The user is already a teacher!")
            except:
                await bot.send_message(message.from_user.id, "The user blocked the bot")

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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()

# endregion


@dp.message_handler(state=Change.CHANGE_0)
async def name_change(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
        if only_letters(message.text) == True:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET real_name = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
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
    else:
        # english
        if only_letters(message.text) == True:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET real_name = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        else:
            await bot.send_message(message.from_user.id, messages.message_error2_en)


# region registerHandler

# start
@dp.message_handler(state=Register.REGISTER_0)
async def register_1(message: types.Message):
    switch_text = message.text.lower()
    is_succeed = False
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users(chat_id, name, `7utra`) values ({message.from_user.id}, '{message.from_user.username}', '{0}')")
    conn.commit()
    conn.close()
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT is_teacher FROM admins WHERE user_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    if result_set != []:
        is_succeed = True
    if message.from_user.username != None:
        if is_succeed == True:
            if switch_text == "en🇬🇧":
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET ru = '{False}' WHERE chat_id = '{message.from_user.id}'")
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Register.all()[1])
                await message.reply(messages.select_en, reply=False, reply_markup=KeyBoards.greet_kb_en)
            elif switch_text == "ru🇷🇺":
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET ru = '{True}' WHERE chat_id = '{message.from_user.id}'")
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Register.all()[1])
                await message.reply(messages.select, reply=False, reply_markup=KeyBoards.greet_kb)
            else:
                await bot.send_message(message.from_user.id, messages.what)
        else:
            if switch_text == "en🇬🇧":
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET ru = '{False}' WHERE chat_id = '{message.from_user.id}'")
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Register.all()[1])
                await message.reply(messages.select_en, reply=False, reply_markup=KeyBoards.greet_kb2_en)
            elif switch_text == "ru🇷🇺":
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET ru = '{True}' WHERE chat_id = '{message.from_user.id}'")
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Register.all()[1])
                await message.reply(messages.select, reply=False, reply_markup=KeyBoards.greet_kb2)
            else:
                await bot.send_message(message.from_user.id, messages.what)
    else:
        if is_succeed == True:
            if switch_text == "en🇬🇧":
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET ru = '{False}' WHERE chat_id = '{message.from_user.id}'")
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Register.all()[1])
                await message.reply(messages.select_en, reply=False, reply_markup=KeyBoards.greet_kb_en)
            elif switch_text == "ru🇷🇺":
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET ru = '{True}' WHERE chat_id = '{message.from_user.id}'")
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Register.all()[1])
                await message.reply(messages.select, reply=False, reply_markup=KeyBoards.greet_kb)
            else:
                await bot.send_message(message.from_user.id, messages.what)
        else:
            if switch_text == "en🇬🇧":
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET ru = '{False}' WHERE chat_id = '{message.from_user.id}'")
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Register.all()[1])
                await message.reply(messages.select_en, reply=False, reply_markup=KeyBoards.greet_kb2_en)
            elif switch_text == "ru🇷🇺":
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET ru = '{True}' WHERE chat_id = '{message.from_user.id}'")
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(Register.all()[1])
                await message.reply(messages.select, reply=False, reply_markup=KeyBoards.greet_kb2)
            else:
                await bot.send_message(message.from_user.id, messages.what)


@dp.message_handler(state=Register.REGISTER_1)
async def register_1(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":

        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
        if switch_text == "я студент":
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(Register.all()[2])
            await message.reply(messages.student_name)
        elif switch_text == "я преподаватель":
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(Register.all()[5])
            await message.reply(messages.teacher_surname)
        else:
            await bot.send_message(message.from_user.id, messages.what)
    else:
        if switch_text == "i'm a student":
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(Register.all()[2])
            await message.reply(messages.student_name_en)
        elif switch_text == "i'm a teacher":
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(Register.all()[5])
            await message.reply(messages.teacher_surname_en)
        else:
            await bot.send_message(message.from_user.id, messages.what_en)


# name
@dp.message_handler(state=Register.REGISTER_2)
async def register_2(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
        if only_letters(message.text) == True:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET real_name = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(Register.all()[3])
            await message.reply(messages.institute_message, reply=False, reply_markup=KeyBoards.institute_kb)
        else:
            await bot.send_message(message.from_user.id, messages.message_error2_en)
    else:
        if only_letters(message.text) == True:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET real_name = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
            conn.commit()
            conn.close()
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(Register.all()[3])
            await message.reply(messages.institute_message_en, reply=False, reply_markup=KeyBoards.institute_kb)
        else:
            await bot.send_message(message.from_user.id, messages.message_error2_en)


# inst
@dp.message_handler(state=Register.REGISTER_3)
async def register_2(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
                    await state.set_state(Register.all()[4])
                else:
                    await bot.send_message(message.from_user.id, messages.message_error)
        except KeyError:
            await bot.send_message(message.from_user.id, messages.message_error)
    else:
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
                    await message.reply(messages.group_message_en, reply_markup=keyboard)
                    state = dp.current_state(user=message.from_user.id)
                    await state.set_state(Register.all()[4])
                else:
                    await bot.send_message(message.from_user.id, messages.message_error_en)
        except KeyError:
            await bot.send_message(message.from_user.id, messages.message_error_en)


# group
@dp.message_handler(state=Register.REGISTER_4)
async def register_3(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
                    f"UPDATE users SET user_group = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
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
                    f"UPDATE users SET user_group = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
                cursor.execute(f"SELECT user_id FROM admins")
                result_set = cursor.fetchall()
                cursor.close()
                is_succeed = False
                for item in result_set:
                    if item[0] == message.from_user.id:
                        is_succeed = True
                if is_succeed:
                    await message.reply(messages.end_of_registration_message_en
                                        , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                    conn.commit()
                    conn.close()
                    state = dp.current_state(user=message.from_user.id)
                    await state.reset_state()
                else:
                    await message.reply(messages.end_of_registration_message_en
                                        , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                    conn.commit()
                    conn.close()
                    state = dp.current_state(user=message.from_user.id)
                    await state.reset_state()
            else:
                await bot.send_message(message.from_user.id, messages.message_error6_en)
        else:
            await bot.send_message(message.from_user.id, messages.message_error6_en)


@dp.message_handler(state=Register.REGISTER_5)
async def register_4(message: types.message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
        url = "http://edu.sfu-kras.ru/timetable/teachers/autocomplete/"
        surname = message.text
        response = requests.get(url + surname).json()
        keyboard = ReplyKeyboardMarkup()
        if len(response) != 0:
            for item in response:
                keyboard.add(item)
                incoming_inst.append(item)
            await message.reply(messages.select, reply_markup=keyboard)
            await dp.current_state(user=message.from_user.id).set_state(Register.all()[6])
        else:
            await message.reply(messages.error, reply_markup=keyboard)
    else:
        url = "http://edu.sfu-kras.ru/timetable/teachers/autocomplete/"
        surname = message.text
        response = requests.get(url + surname).json()
        keyboard = ReplyKeyboardMarkup()
        if len(response) != 0:
            for item in response:
                keyboard.add(item)
                incoming_inst.append(item)
            await message.reply(messages.select_en, reply_markup=keyboard)
            await dp.current_state(user=message.from_user.id).set_state(Register.all()[6])
        else:
            await message.reply(messages.error_en, reply_markup=keyboard)


@dp.message_handler(state=Register.REGISTER_6)
async def register_5(message: types.message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
                    f"UPDATE users SET real_name = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
                cursor.execute(
                    f"UPDATE users SET user_group = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
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
                    f"UPDATE users SET real_name = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
                cursor.execute(
                    f"UPDATE users SET user_group = '{message.text}' WHERE chat_id = '{message.from_user.id}'")
                cursor.execute(f"UPDATE users SET is_teacher = '{True}' WHERE chat_id = '{message.from_user.id}'")
                cursor.execute(f"SELECT user_id FROM admins")
                result_set = cursor.fetchall()
                cursor.close()
                is_succeed = False
                for item in result_set:
                    if item[0] == message.from_user.id:
                        is_succeed = True
                if is_succeed:
                    await message.reply(messages.end_of_registration_message_en
                                        , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                    conn.commit()
                    conn.close()
                    state = dp.current_state(user=message.from_user.id)
                    await state.reset_state()
                else:
                    await message.reply(messages.end_of_registration_message_en
                                        , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                    conn.commit()
                    conn.close()
                    state = dp.current_state(user=message.from_user.id)
                    await state.reset_state()
            else:
                await bot.send_message(message.from_user.id, messages.message_error3_en)
        else:
            await bot.send_message(message.from_user.id, messages.message_error3_en)


# endregion


# region schedule_userHandler
@dp.message_handler(state=ScheduleUser.SCHEDULE_USER_0)
async def schedule_0(msg: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{msg.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = msg.text.lower()
    if is_ru == True:
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
    else:
        # english
        try:
            if messages.institutes[msg.text]:
                if only_letters(msg.text) == True:
                    inst = messages.institutes[msg.text]
                    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add("Menu")
                    url = 'https://edu.sfu-kras.ru/api/timetable/groups'
                    response = requests.get(url).json()
                    for item in response:
                        if item['institute'] == inst:
                            keyboard.add(item['name'])
                            incoming_inst.append(item['name'])
                    await msg.reply(messages.group_message_en, reply_markup=keyboard)
                    state = dp.current_state(user=msg.from_user.id)
                    await state.set_state(ScheduleUser.all()[1])
                else:
                    await bot.send_message(msg.from_user.id, messages.message_error_en)
        except KeyError:
            await bot.send_message(msg.from_user.id, messages.message_error_en)


@dp.message_handler(state=ScheduleUser.SCHEDULE_USER_1)
async def schedule_1(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
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
                    await message.reply(messages.day_of_the_week_en, reply_markup=KeyBoards.day_of_the_week_kb_en)
                    state = dp.current_state(user=message.from_user.id)
                    await state.set_state(ScheduleUser.all()[2])
                else:
                    await bot.send_message(message.from_user.id, messages.message_error6_en)
            else:
                await bot.send_message(message.from_user.id, messages.message_error6_en)


@dp.message_handler(state=ScheduleUser.SCHEDULE_USER_2)
async def schedule_1(message: types.Message):
    global group
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Понедельник</b>\n\t\t➖➖➖➖➖➖➖'
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
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Вторник</b>\n\t\t➖➖➖➖➖➖➖'
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
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Среда</b>\n\t\t➖➖➖➖➖➖➖'
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
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Четверг</b>\n\t\t➖➖➖➖➖➖➖'
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
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Пятница</b>\n\t\t➖➖➖➖➖➖➖'
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
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Суббота</b>\n\t\t➖➖➖➖➖➖➖'
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
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        else:
            if switch_text == "monday":
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
                        timetable_message += "It is now <b>odd</b> week\n"
                    else:
                        timetable_message += "It is now <b>an even</b> week\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Monday</b>\n\t\t➖➖➖➖➖➖➖'
                    for i in adding:
                        if i[0] == '1':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'On Monday, this group has no couples!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "tuesday":
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
                        timetable_message += "It is now <b>odd</b> week\n"
                    else:
                        timetable_message += "It is now <b>an even</b> week\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Tuesday</b>\n\t\t➖➖➖➖➖➖➖'
                    for i in adding:
                        if i[0] == '2':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'On Tuesday, this group has no couples!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "wednesday":
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
                        timetable_message += "It is now <b>odd</b> week\n"
                    else:
                        timetable_message += "It is now <b>an even</b> week\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Wednesday</b>\n\t\t➖➖➖➖➖➖➖'
                    for i in adding:
                        if i[0] == '3':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'On Wednesday, this group has no pairs!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "thursday":
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
                        timetable_message += "It is now <b>odd</b> week\n"
                    else:
                        timetable_message += "It is now <b>an even</b> week\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Thursday</b>\n\t\t➖➖➖➖➖➖➖'
                    for i in adding:
                        if i[0] == '4':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'On Thursday, this group has no couples!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "friday":
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
                        timetable_message += "It is now <b>odd</b> week\n"
                    else:
                        timetable_message += "It is now <b>an even</b> week\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Friday</b>\n\t\t➖➖➖➖➖➖➖'
                    for i in adding:
                        if i[0] == '5':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'On Friday, this group has no couples!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "saturday":
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
                        timetable_message += "It is now <b>odd</b> week\n"
                    else:
                        timetable_message += "It is now <b>an even</b> week\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Saturday</b>\n\t\t➖➖➖➖➖➖➖'
                    for i in adding:
                        if i[0] == '6':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'On Saturday, this group has no couples!'
                await message.reply(timetable_message, parse_mode="HTML")
            elif switch_text == "view next week's schedule":
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(ScheduleUser.all()[3])
                await message.reply("Choose a day of the week 👇\n(You'll be watching next week)"
                                    , reply=False, reply_markup=KeyBoards.day_of_the_week_kb2_en)
            else:
                await bot.send_message(message.from_user.id, messages.what_en)


@dp.message_handler(state=ScheduleUser.SCHEDULE_USER_3)
async def schedule_1(message: types.Message):
    global group
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Понедельник</b>\n\t\t➖➖➖➖➖➖➖'
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
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Вторник</b>\n\t\t➖➖➖➖➖➖➖'
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
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Среда</b>\n\t\t➖➖➖➖➖➖➖'
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
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Четверг</b>\n\t\t➖➖➖➖➖➖➖'
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
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Пятница</b>\n\t\t➖➖➖➖➖➖➖'
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
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Суббота</b>\n\t\t➖➖➖➖➖➖➖'
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
    else:
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        # english
        else:
            if switch_text == "monday":
                timetable_message = ""
                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
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
                        timetable_message += "It is now <b>odd</b> week\n"
                    else:
                        timetable_message += "It is now <b>an even</b> week\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Monday</b>\n\t\t➖➖➖➖➖➖➖'
                    for i in adding:
                        if i[0] == '1':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'On Monday, this group has no couples!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "tuesday":
                timetable_message = ""

                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
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
                        timetable_message += "It is now <b>odd</b> week\n"
                    else:
                        timetable_message += "It is now <b>an even</b> week\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Tuesday</b>\n\t\t➖➖➖➖➖➖➖'
                    for i in adding:
                        if i[0] == '2':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'On Tuesday, this group has no couples!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "wednesday":
                timetable_message = ""

                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
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
                        timetable_message += "It is now <b>odd</b> week\n"
                    else:
                        timetable_message += "It is now <b>an even</b> week\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Wednesday</b>\n\t\t➖➖➖➖➖➖➖'
                    for i in adding:
                        if i[0] == '3':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'On Wednesday, this group has no pairs!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "thursday":
                timetable_message = ""

                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
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
                        timetable_message += "It is now <b>odd</b> week\n"
                    else:
                        timetable_message += "It is now <b>an even</b> week\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Thursday</b>\n\t\t➖➖➖➖➖➖➖'
                    for i in adding:
                        if i[0] == '4':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'On Thursday, this group has no couples!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "friday":
                timetable_message = ""

                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
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
                        timetable_message += "It is now <b>odd</b> week\n"
                    else:
                        timetable_message += "It is now <b>an even</b> week\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Friday</b>\n\t\t➖➖➖➖➖➖➖'
                    for i in adding:
                        if i[0] == '5':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'On Friday, this group has no couples!'
                await message.reply(timetable_message, parse_mode="HTML")

            elif switch_text == "saturday":
                timetable_message = ""

                url = 'https://edu.sfu-kras.ru/timetable'
                response = requests.get(url).text
                match = re.search(r'Идёт\s\w{8}\sнеделя', response)
                if match:
                    current_week = "2"
                else:
                    current_week = "1"
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
                        timetable_message += "It is now <b>odd</b> week\n"
                    else:
                        timetable_message += "It is now <b>an even</b> week\n"
                    timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Saturday</b>\n\t\t➖➖➖➖➖➖➖'
                    for i in adding:
                        if i[0] == '6':
                            if i[4] == '' and i[5] == '':
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                            else:
                                timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                else:
                    timetable_message += 'On Saturday, this group has no couples!'
                await message.reply(timetable_message, parse_mode="HTML")
            elif switch_text == 'view the schedule for the current week':
                state = dp.current_state(user=message.from_user.id)
                await state.set_state(ScheduleUser.all()[2])
                await message.reply("Choose a day of the week 👇\n(You will be watching this week)"
                                    , reply=False, reply_markup=KeyBoards.day_of_the_week_kb_en)
            else:
                await bot.send_message(message.from_user.id, messages.what_en)


# endregion

@dp.message_handler(state=Schedule.SCHEDULE_0)
async def schedule(message: types.Message):
    global group
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '1':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Понедельник</b>\n\t\t➖➖➖➖➖➖➖'
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '2':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Вторник</b>\n\t\t➖➖➖➖➖➖➖'
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '3':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Среда</b>\n\t\t➖➖➖➖➖➖➖'
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '4':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Четверг</b>\n\t\t➖➖➖➖➖➖➖'
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '5':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Пятница</b>\n\t\t➖➖➖➖➖➖➖'
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '6':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        timetable_message += "Вы смотрите расписание на <b>следующую</b> неделю\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Суббота</b>\n\t\t➖➖➖➖➖➖➖'
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Понедельник</b>\n\t\t➖➖➖➖➖➖➖'
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Вторник</b>\n\t\t➖➖➖➖➖➖➖'
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Среда</b>\n\t\t➖➖➖➖➖➖➖'
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Четверг</b>\n\t\t➖➖➖➖➖➖➖'
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Пятница</b>\n\t\t➖➖➖➖➖➖➖'
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Суббота</b>\n\t\t➖➖➖➖➖➖➖'
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
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
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
                if switch_text == 'monday':
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '1':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        timetable_message += "You are looking at the schedule for the <b>next</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Monday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '1':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'Next Monday, there are no couples! A great reason to see your friends! 🎉'
                    await message.reply(timetable_message, parse_mode="HTML")

                elif switch_text == 'tuesday':
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '2':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        timetable_message += "You are looking at the schedule for the <b>next</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Tuesday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '2':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'Next Tuesday, there are no couples! A great reason to see your friends! 🎉'
                    await message.reply(timetable_message, parse_mode="HTML")

                elif switch_text == 'wednesday':
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '3':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        timetable_message += "You are looking at the schedule for the <b>next</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Wednesday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '3':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'Next Wednesday, there are no couples! A great reason to see your friends! 🎉'
                    await message.reply(timetable_message, parse_mode="HTML")

                elif switch_text == 'thursday':
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '4':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        timetable_message += "You are looking at the schedule for the <b>next</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Thursday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '4':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'Next Thursday, there are no couples! A great reason to see your friends! 🎉'
                    await message.reply(timetable_message, parse_mode="HTML")

                elif switch_text == 'friday':
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '5':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        timetable_message += "You are looking at the schedule for the <b>next</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Friday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '5':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'Next Friday, there are no couples! A great reason to see your friends! 🎉'
                    await message.reply(timetable_message, parse_mode="HTML")

                elif switch_text == 'saturday':
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '6':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        timetable_message += "You are looking at the schedule for the <b>next</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Saturday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '6':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'Next Saturday, there are no couples! A great reason to see your friends! 🎉'
                    await message.reply(timetable_message, parse_mode="HTML")
                elif switch_text == 'view the schedule for the current week':
                    state = dp.current_state(user=message.from_user.id)
                    await state.set_state(CheckSchedule.all()[0])
                    await message.reply('Select the day of the week 👇\n(You will be watching the current week)'
                                        , reply=False, reply_markup=KeyBoards.day_of_the_week_kb_en)

                else:
                    await bot.send_message(message.from_user.id, messages.what_en)
            else:
                if switch_text == 'monday':
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
                        timetable_message += "You are looking at the schedule for the <b>next</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Monday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '1':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'Next Monday you have no couples!'
                    await message.reply(timetable_message, parse_mode="HTML")

                elif switch_text == 'tuesday':
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
                        timetable_message += "You are looking at the schedule for the <b>next</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Tuesday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '2':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'Next Tuesday you have no couples!'
                    await message.reply(timetable_message, parse_mode="HTML")

                elif switch_text == 'wednesday':
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
                        timetable_message += "You are looking at the schedule for the <b>next</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Wednesday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '3':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'Next Wednesday you have no couples!'
                    await message.reply(timetable_message, parse_mode="HTML")

                elif switch_text == 'thursday':
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
                        timetable_message += "You are looking at the schedule for the <b>next</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Thursday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '4':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'Next Thursday you have no couples!'
                    await message.reply(timetable_message, parse_mode="HTML")

                elif switch_text == 'friday':
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
                        timetable_message += "You are looking at the schedule for the <b>next</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Friday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '5':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'Next Friday you have no couples!'
                    await message.reply(timetable_message, parse_mode="HTML")

                elif switch_text == 'saturday':
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
                        timetable_message += "You are looking at the schedule for the <b>next</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Saturday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '6':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'Next Saturday you have no couples!'
                    await message.reply(timetable_message, parse_mode="HTML")
                elif switch_text == 'view the schedule for the current week':
                    state = dp.current_state(user=message.from_user.id)
                    await state.set_state(CheckSchedule.all()[0])
                    await message.reply('Select the day of the week 👇\n(You will be watching the current week)'
                                        , reply=False, reply_markup=KeyBoards.day_of_the_week_kb_en)
                else:
                    await bot.send_message(message.from_user.id, messages.what_en)


@dp.message_handler(state=CheckSchedule.SCH_0)
async def schedule_check(msg: types.Message):
    global group
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{msg.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = msg.text.lower()
    if is_ru == True:
        if msg.text.lower() == "меню":
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Понедельник</b>\n\t\t➖➖➖➖➖➖➖'
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Вторник</b>\n\t\t➖➖➖➖➖➖➖'
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Среда</b>\n\t\t➖➖➖➖➖➖➖'
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Четверг</b>\n\t\t➖➖➖➖➖➖➖'
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Пятница</b>\n\t\t➖➖➖➖➖➖➖'
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Суббота</b>\n\t\t➖➖➖➖➖➖➖'
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Понедельник</b>\n\t\t➖➖➖➖➖➖➖'
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Вторник</b>\n\t\t➖➖➖➖➖➖➖'
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Среда</b>\n\t\t➖➖➖➖➖➖➖'
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Четверг</b>\n\t\t➖➖➖➖➖➖➖'
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Пятница</b>\n\t\t➖➖➖➖➖➖➖'
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
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Суббота</b>\n\t\t➖➖➖➖➖➖➖'
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
    else:
        # english
        if msg.text.lower() == "menu":
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
                await msg.reply(messages.menu_en
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=msg.from_user.id)
                await state.reset_state()
            else:
                await msg.reply(messages.menu_en
                                , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=msg.from_user.id)
                await state.reset_state()
        else:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT is_teacher FROM users WHERE chat_id = '{msg.from_user.id}'")
            teacher = cursor.fetchall()[0][0]
            switch_text = msg.text.lower()
            if not teacher:
                if switch_text == "monday":
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '1':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        if match:
                            timetable_message += "Now it is <b>odd</b> week\n"
                        else:
                            timetable_message += "It is now <b>an even</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Monday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '1':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'No couples on Monday! A great reason to see your friends! 🎉'
                    await msg.reply(timetable_message, parse_mode="HTML")

                elif switch_text == "tuesday":
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '2':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        if match:
                            timetable_message += "Now it is <b>odd</b> week\n"
                        else:
                            timetable_message += "It is now <b>an even</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Tuesday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '2':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'

                    else:
                        timetable_message += 'No couples on Tuesday! A great reason to see your friends! 🎉'
                    await msg.reply(timetable_message, parse_mode="HTML")

                elif switch_text == "wednesday":
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '3':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        if match:
                            timetable_message += "Now it is <b>odd</b> week\n"
                        else:
                            timetable_message += "It is now <b>an even</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Wednesday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '3':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'No couples on Wednesday! A great reason to see your friends! 🎉'
                    await msg.reply(timetable_message, parse_mode="HTML")

                elif switch_text == "thursday":
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '4':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        if match:
                            timetable_message += "Now it is <b>odd</b> week\n"
                        else:
                            timetable_message += "It is now <b>an even</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Thursday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '4':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'No couples on Thursday! A great reason to see your friends! 🎉'
                    await msg.reply(timetable_message, parse_mode="HTML")

                elif switch_text == "friday":
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '5':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        if match:
                            timetable_message += "Now it is <b>odd</b> week\n"
                        else:
                            timetable_message += "It is now <b>an even</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Friday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '5':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'No couples on Friday! A great reason to see your friends! 🎉'
                    await msg.reply(timetable_message, parse_mode="HTML")

                elif switch_text == "saturday":
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
                                [item['day'], item['time'], item['subject'], item['type'], item['teacher'],
                                 item['place']])
                    flag = 0
                    for i in adding:
                        if i[0] == '6':
                            if i[2] != '':
                                flag = 1
                    if flag == 1:
                        if match:
                            timetable_message += "Now it is <b>odd</b> week\n"
                        else:
                            timetable_message += "It is now <b>an even</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Saturday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '6':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += 'No couples on Saturday! A great reason to see your friends! 🎉'
                    await msg.reply(timetable_message, parse_mode="HTML")
                elif switch_text == "view next week's schedule":
                    state = dp.current_state(user=msg.from_user.id)
                    await state.set_state(Schedule.all()[0])
                    await msg.reply('Choose the day of the week 👇\n(You will watch the next week)'
                                    , reply=False, reply_markup=KeyBoards.day_of_the_week_kb2_en)
                else:
                    if msg.text != "View next week's schedule":
                        await bot.send_message(msg.from_user.id, messages.what_en)
            else:
                if switch_text == "monday":
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
                            timetable_message += "Now it is <b>odd</b> week\n"
                        else:
                            timetable_message += "It is now <b>an even</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Monday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '1':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += "You don't have any couples on Monday!"
                    await msg.reply(timetable_message, parse_mode="HTML")

                elif switch_text == "tuesday":
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
                            timetable_message += "Now it is <b>odd</b> week\n"
                        else:
                            timetable_message += "It is now <b>an even</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Tuesday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '2':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += "You don't have any couples on Tuesday!"
                    await msg.reply(timetable_message, parse_mode="HTML")

                elif switch_text == "wednesday":
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
                            timetable_message += "Now it is <b>odd</b> week\n"
                        else:
                            timetable_message += "It is now <b>an even</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Wednesday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '3':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += "You don't have any couples on Wednesday!"
                    await msg.reply(timetable_message, parse_mode="HTML")

                elif switch_text == "thursday":
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
                            timetable_message += "Now it is <b>odd</b> week\n"
                        else:
                            timetable_message += "It is now <b>an even</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Thursday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '4':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += "You don't have any couples on Thursday!"
                    await msg.reply(timetable_message, parse_mode="HTML")

                elif switch_text == "friday":
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
                            timetable_message += "Now it is <b>odd</b> week\n"
                        else:
                            timetable_message += "It is now <b>an even</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Friday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '5':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += "You don't have any couples on Friday!"
                    await msg.reply(timetable_message, parse_mode="HTML")

                elif switch_text == "saturday":
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
                            timetable_message += "Now it is <b>odd</b> week\n"
                        else:
                            timetable_message += "It is now <b>an even</b> week\n"
                        timetable_message += '\n\t\t\t\t\t\t\t\t\t<b>Saturday</b>\n\t\t➖➖➖➖➖➖➖'
                        for i in adding:
                            if i[0] == '6':
                                if i[4] == '' and i[5] == '':
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])})\n'
                                else:
                                    timetable_message += f'\n{i[1]}\n{translate(i[2])} ({translate(i[3])}) \n{translate(i[4])}\n<b>{i[5]}</b>\n'
                    else:
                        timetable_message += "You don't have any couples on Saturday!"
                    await msg.reply(timetable_message, parse_mode="HTML")
                elif switch_text == "view next week's schedule":
                    state = dp.current_state(user=msg.from_user.id)
                    await state.set_state(Schedule.all()[0])
                    await msg.reply('Choose the day of the week 👇\n(You will watch the next week)'
                                    , reply=False, reply_markup=KeyBoards.day_of_the_week_kb2_en)
                else:
                    await bot.send_message(msg.from_user.id, messages.what_en)

        conn.close()


@dp.message_handler(state=Delete.DELETE_EVENTS_0)
async def schedule(message: types.Message):
    global group
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
            a = False
            for i in incoming_inst2:
                if i == message.text:
                    a = True
            if only_letters(message.text) == True:
                if a == True:
                    incoming_inst2.clear()
                    state = dp.current_state(user=message.from_user.id)
                    await state.set_state(Delete.all()[3])
                    incoming_events2[message.from_user.id] = message.text
                    await message.reply(messages.events_del
                                        , reply=False, reply_markup=KeyBoards.yes_or_no_keyboard2)
                else:
                    await bot.send_message(message.from_user.id, messages.message_error7)
            else:
                await bot.send_message(message.from_user.id, messages.message_error7)
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()

        elif switch_text == "add an event":
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(Events.all()[0])
            await message.reply(messages.events_write_en, reply_markup=KeyBoards.universal_kb_en)

        else:
            a = False
            for i in incoming_inst2:
                if i == message.text:
                    a = True
            if only_letters(message.text) == True:
                if a == True:
                    incoming_inst2.clear()
                    state = dp.current_state(user=message.from_user.id)
                    await state.set_state(Delete.all()[3])
                    incoming_events2[message.from_user.id] = message.text
                    await message.reply(messages.events_del_en
                                        , reply=False, reply_markup=KeyBoards.yes_or_no_keyboard2_en)
                else:
                    await bot.send_message(message.from_user.id, messages.message_error7_en)
            else:
                await bot.send_message(message.from_user.id, messages.message_error7_en)


@dp.message_handler(state=Delete.DELETE_EVENTS_1)
async def schedule(message: types.Message):
    global group
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
            for i in incoming_inst2:
                if i == message.text:
                    a = True
            if only_letters(message.text) == True:
                if a == True:
                    incoming_inst2.clear()
                    state = dp.current_state(user=message.from_user.id)
                    incoming_events2[message.from_user.id] = message.text
                    await state.set_state(Delete.all()[2])
                    await message.reply(messages.mailing_del
                                        , reply=False, reply_markup=KeyBoards.yes_or_no_keyboard2)
                else:
                    await bot.send_message(message.from_user.id, messages.message_error8)
            else:
                await bot.send_message(message.from_user.id, messages.message_error8)
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        else:
            a = False
            for i in incoming_inst2:
                if i == message.text:
                    a = True
            if only_letters(message.text) == True:
                if a == True:
                    incoming_inst2.clear()
                    state = dp.current_state(user=message.from_user.id)
                    incoming_events2[message.from_user.id] = message.text
                    await state.set_state(Delete.all()[2])
                    await message.reply(messages.mailing_del_en
                                        , reply=False, reply_markup=KeyBoards.yes_or_no_keyboard2_en)
                else:
                    await bot.send_message(message.from_user.id, messages.message_error8_en)
            else:
                await bot.send_message(message.from_user.id, messages.message_error8_en)


@dp.message_handler(state=Delete.DELETE_EVENTS_2)
async def schedule(message: types.Message):
    global group
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
        else:
            await bot.send_message(message.from_user.id, messages.what)
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        elif switch_text == 'yes':
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM `mail` WHERE (`chat_id` ==  {message.from_user.id} AND `event1` == '{incoming_events2[message.from_user.id]}');")
            incoming_events2.pop(message.from_user.id)
            conn.commit()
            conn.close()
            await bot.send_message(message.from_user.id, messages.successfully_en)
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        else:
            await bot.send_message(message.from_user.id, messages.what_en)


@dp.message_handler(state=Delete.DELETE_EVENTS_3)
async def schedule(message: types.Message):
    global group
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
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
        else:
            await bot.send_message(message.from_user.id, messages.what)
    else:
        # english
        if switch_text == 'menu':
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        elif switch_text == 'yes':
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM `times` WHERE (`chat_id` ==  {message.from_user.id} AND `event1` == '{incoming_events2[message.from_user.id]}');")
            incoming_events2.pop(message.from_user.id)
            conn.commit()
            conn.close()
            await bot.send_message(message.from_user.id, messages.successfully_en)
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
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
            else:
                await message.reply(messages.menu_en
                                    , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=message.from_user.id)
                await state.reset_state()
        else:
            await bot.send_message(message.from_user.id, messages.what_en)


@dp.message_handler(state=Change_Eu_Rus.CHANGE_RUS_EN_0)
async def name_change(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{message.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = message.text.lower()
    if is_ru == True:
        if only_letters(message.text) == True:
            if switch_text == 'да':
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET ru = '{False}' WHERE chat_id = '{message.from_user.id}'")
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
                    await message.reply(messages.menu_en
                                        , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                    conn.commit()
                    conn.close()
                    state = dp.current_state(user=message.from_user.id)
                    await state.reset_state()
                else:
                    await message.reply(messages.menu_en
                                        , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                    conn.commit()
                    conn.close()
                    state = dp.current_state(user=message.from_user.id)
                    await state.reset_state()

            elif switch_text == 'меню':
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
                await bot.send_message(message.from_user.id, "Похоже, что вы допустили ошибку, попробуйте еще раз ❌")
    else:
        # english
        if only_letters(message.text) == True:
            if switch_text == 'yes':
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET ru = '{True}' WHERE chat_id = '{message.from_user.id}'")
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

            elif switch_text == 'menu':
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
                                        , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                    conn.commit()
                    conn.close()
                    state = dp.current_state(user=message.from_user.id)
                    await state.reset_state()
                else:
                    await message.reply(messages.menu
                                        , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                    conn.commit()
                    conn.close()
                    state = dp.current_state(user=message.from_user.id)
                    await state.reset_state()
            else:
                await bot.send_message(message.from_user.id, 'It looks like you made a mistake, please try again ❌')


@dp.message_handler(state='*', content_types=["text"])
async def handler_message(msg: types.Message):
    global adding, message
    global group
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{msg.from_user.id}'")
    result_set = cursor.fetchall()
    cursor.close()
    is_ru = False
    if result_set[0][0] == "True":
        is_ru = True
    switch_text = msg.text.lower()
    if is_ru == True:
        if switch_text == "расписание":
            await dp.current_state(user=msg.from_user.id).set_state(CheckSchedule.all()[0])
            await msg.reply(messages.day_of_the_week, reply_markup=KeyBoards.day_of_the_week_kb)

        elif switch_text == "админ-панель":
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT user_id FROM admins")
            result_set = cursor.fetchall()
            cursor.execute(f"SELECT user_id, is_teacher FROM admins")
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
                        local_time[0] = "Четверг"
                    if local_time[0] == "Fri":
                        local_time[0] = "Пятница"
                    if local_time[0] == "Sat":
                        local_time[0] = "Суббота"
                    if local_time[0] == "Sun":
                        local_time[0] = "Воскресенье"
                    # месяц
                    if local_time[1] == "Jun":
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
                        list = local_time[4].split(':')
                        k = int(list[0]) + 7
                        if k > 24:
                            k = k - 24
                        elif k == 24:
                            k = "0"
                        a = a + f" - <b>{item[1]}</b>" + '\n' + \
                            f'Эта рассылка заканчивается {local_time[3]} {local_time[1]} ' \
                            f'({local_time[0]}) {local_time[5]} года в {k}:{list[1]}' + '\n'
                    else:
                        list = local_time[3].split(':')
                        k = int(list[0]) + 7
                        if k > 24:
                            k = k - 24
                        elif k == 24:
                            k = "0"
                        a = a + f" - <b>{item[1]}</b>" + '\n' + \
                            f'Эта рассылка заканчивается {local_time[2]} {local_time[1]} ' \
                            f'({local_time[0]}) {local_time[4]} года в {k}:{list[1]}' + '\n'
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
                        local_time[0] = "Четверг"
                    if local_time[0] == "Fri":
                        local_time[0] = "Пятница"
                    if local_time[0] == "Sat":
                        local_time[0] = "Суббота"
                    if local_time[0] == "Sun":
                        local_time[0] = "Воскресенье"
                    # месяц
                    if local_time[1] == "Jun":
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
                        list = local_time[4].split(':')
                        k = int(list[0]) + 7
                        if k > 24:
                            k = k - 24
                        elif k == 24:
                            k = "0"
                        a = a + f" - <b>{item[1]}</b>" + '\n' + \
                            f'Это мероприятие заканчивается {local_time[3]} {local_time[1]} ' \
                            f'({local_time[0]}) {local_time[5]} года в {k}:{list[1]}\n'

                    else:
                        list = local_time[3].split(':')
                        k = int(list[0]) + 7
                        if k > 24:
                            k = k - 24
                        elif k == 24:
                            k = "0"
                        a = a + f" - <b>{item[1]}</b>" + '\n' + \
                            f'Это мероприятие заканчивается {local_time[2]} {local_time[1]} ' \
                            f'({local_time[0]}) {local_time[4]} года в {k}:{list[1]}\n'
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
            await state.set_state(Register.all()[5])
            await msg.reply(messages.teacher_surname2)

        elif switch_text == "добавить мероприятие":
            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(Events.all()[0])
            await msg.reply(messages.events_write, reply_markup=KeyBoards.universal_kb)

        elif switch_text == "удалить мероприятие":
            a = False
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM times")
            result_set = cursor.fetchall()
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            for item in result_set:
                if item[0] == msg.from_user.id:
                    keyboard.add(item[1])
                    incoming_inst2.append(item[1])
                    a = True
            if a == True:
                state = dp.current_state(user=msg.from_user.id)
                await state.set_state(Delete.all()[0])
                await msg.reply(messages.choose_event_del, reply_markup=keyboard)
            else:
                await bot.send_message(msg.from_user.id, messages.event_not)

        elif switch_text == "удалить рассылку":
            a = False
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM mail")
            result_set = cursor.fetchall()
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            for item in result_set:
                if item[0] == msg.from_user.id:
                    keyboard.add(item[1])
                    incoming_inst2.append(item[1])
                    a = True
            if a == True:
                state = dp.current_state(user=msg.from_user.id)
                await state.set_state(Delete.all()[1])
                await msg.reply(messages.choose_mail_del, reply_markup=keyboard)
            else:
                await bot.send_message(msg.from_user.id, messages.mail_not)

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
            await state.set_state(Register.all()[3])
            await msg.reply(messages.choose_inst_change, reply_markup=KeyBoards.institute_kb)

        elif switch_text == "посмотреть расписание другой группы":
            await msg.reply(messages.choose_inst, reply_markup=KeyBoards.institute_kb)
            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(ScheduleUser.all()[0])

        elif switch_text == "посмотреть расписание группы":
            await msg.reply(messages.choose_inst, reply_markup=KeyBoards.institute_kb)
            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(ScheduleUser.all()[0])
        elif switch_text == 'поменять язык':
            await msg.reply("Вы точно хотите поменять язык?", reply_markup=KeyBoards.yes_or_no_keyboard2)
            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(Change_Eu_Rus.all()[0])
        elif switch_text == "test":
            await msg.reply(f"{messages.greets_msg}")
        elif switch_text == "выгрузить всю базу данных":
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT user_id FROM admins")
            result_set = cursor.fetchall()
            cursor.close()
            is_succeed = False
            for item in result_set:
                if item[0] == msg.from_user.id:
                    is_succeed = True
            if is_succeed:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM users")
                result_set = cursor.fetchall()
                message = "<b>ID, имя пользователя и имя в боте и группа:</b>\n"
                for i in result_set:
                    message += str(i[0])
                    message += ", "
                    message += str(i[1])
                    message += ", "
                    message += str(i[2])
                    message += ", "
                    message += str(i[3])
                    message += "\n"
                    message += "\n"
                await bot.send_message(msg.from_user.id, message, parse_mode="HTML")
            else:
                await msg.reply(messages.not_admin, reply_markup=KeyBoards.menu_admin_kb)
        else:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{msg.from_user.id}'")
            result_set = cursor.fetchall()
            cursor.close()
            is_ru = False
            if result_set[0][0] == "True":
                is_ru = True
            if is_ru == True:
                await bot.send_message(msg.from_user.id, messages.what)
            else:
                await bot.send_message(msg.from_user.id, messages.what_en)
    else:
        # english
        if switch_text == "schedule":
            await dp.current_state(user=msg.from_user.id).set_state(CheckSchedule.all()[0])
            await msg.reply(messages.day_of_the_week_en, reply_markup=KeyBoards.day_of_the_week_kb_en)

        elif switch_text == "admin panel":
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT user_id FROM admins")
            result_set = cursor.fetchall()
            cursor.execute(f"SELECT user_id, is_teacher FROM admins")
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
                    await msg.reply(messages.admin_panel_en, reply_markup=KeyBoards.admin_panel_teacher_en)
                else:
                    state = dp.current_state(user=msg.from_user.id)
                    await state.set_state(AdminPanel.all()[0])
                    await msg.reply(messages.admin_panel_en, reply_markup=KeyBoards.admin_panel_en)
            else:
                await msg.reply(messages.not_admin_en, reply_markup=KeyBoards.menu_admin_kb_en)
        elif switch_text == "menu":
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
                await msg.reply(messages.menu_en
                                , reply=False, reply_markup=KeyBoards.menu_admin_kb_en)
                conn.commit()
                conn.close()
                state = dp.current_state(user=msg.from_user.id)
                await state.reset_state()
            else:
                await msg.reply(messages.menu_en
                                , reply=False, reply_markup=KeyBoards.menu_user_kb_en)
                conn.commit()
                conn.close()

        elif switch_text == "mailing lists":
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM mail")
            result_set = cursor.fetchall()
            a = "Your mailing lists: \n"
            for item in result_set:
                if item[0] == msg.from_user.id:
                    local_time = time.ctime(item[2])
                    local_time = local_time.split(' ')
                    if local_time[2] == '':
                        list = local_time[4].split(':')
                        k = int(list[0]) + 7
                        if k > 24:
                            k = k - 24
                        elif k == 24:
                            k = "0"
                        a = a + f" - <b>{item[1]}</b>" + '\n' + \
                            f'This newsletter is ending {local_time[3]} {local_time[1]} ' \
                            f'({local_time[0]}) {local_time[5]} years in {k}:{list[1]}' + '\n'
                    else:
                        list = local_time[3].split(':')
                        k = int(list[0]) + 7
                        if k > 24:
                            k = k - 24
                        elif k == 24:
                            k = "0"
                        a = a + f" - <b>{item[1]}</b>" + '\n' + \
                            f'This newsletter is ending {local_time[2]} {local_time[1]} ' \
                            f'({local_time[0]}) {local_time[4]} years in {k}:{list[1]}' + '\n'
            if a == "Your mailing lists: \n":
                a = "You haven't received any mailings yet!"
            await msg.reply(a, reply_markup=KeyBoards.mailing_lists_kb_en, parse_mode="HTML")

        elif switch_text == "profile":
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
                        await bot.send_message(msg.from_user.id, f"Your last name: <b>{i[1]}</b>\n"
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
                        await bot.send_message(msg.from_user.id, f"Your name: <b>{i[1]}</b>\n"
                                                                 f"Your institute: <i><b>{translate(i[2])}</b></i> 🎓\n"
                                                                 f"Your group: <i><b>{i[3]}</b></i> 🎓"
                                               , parse_mode="HTML")
                conn.commit()
                conn.close()
        elif switch_text == "settings":
            await msg.reply(messages.settings_en, reply_markup=KeyBoards.setting_kb_en)

        elif switch_text == "planned events":
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM times")
            result_set = cursor.fetchall()
            a = "Your events: \n"
            for item in result_set:
                if item[0] == msg.from_user.id:
                    local_time = time.ctime(item[2])
                    local_time = local_time.split(' ')
                    # день недели
                    if local_time[2] == '':
                        list = local_time[4].split(':')
                        k = int(list[0]) + 7
                        if k > 24:
                            k = k - 24
                        elif k == 24:
                            k = "0"
                        a = a + f" - <b>{item[1]}</b>" + '\n' + \
                            f'This event ends {local_time[3]} {local_time[1]} ' \
                            f'({local_time[0]}) {local_time[5]} years in {k}:{list[1]}\n'

                    else:
                        list = local_time[3].split(':')
                        k = int(list[0]) + 7
                        if k > 24:
                            k = k - 24
                        elif k == 24:
                            k = "0"
                        a = a + f" - <b>{item[1]}</b>" + '\n' + \
                            f'This event ends {local_time[2]} {local_time[1]} ' \
                            f'({local_time[0]}) {local_time[4]} years in {k}:{list[1]}\n'
            if a == "Your events: \n":
                a = "You don't have any events!"
            await msg.reply(a, reply_markup=KeyBoards.events_kb_en, parse_mode="HTML")

        elif switch_text == "change information":
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
                await msg.reply(messages.choose_want_change_en, reply_markup=KeyBoards.change_information_kb2_en)
            else:
                await msg.reply(messages.choose_want_change_en, reply_markup=KeyBoards.change_information_kb_en)

        elif switch_text == "change the teacher":
            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(Register.all()[5])
            await msg.reply(messages.teacher_surname_en2)

        elif switch_text == "add an event":
            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(Events.all()[0])
            await msg.reply(messages.events_write_en, reply_markup=KeyBoards.universal_kb_en)

        elif switch_text == "delete an event":
            a = False
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM times")
            result_set = cursor.fetchall()
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            for item in result_set:
                if item[0] == msg.from_user.id:
                    keyboard.add(item[1])
                    incoming_inst2.append(item[1])
                    a = True
            if a == True:
                state = dp.current_state(user=msg.from_user.id)
                await state.set_state(Delete.all()[0])
                await msg.reply(messages.choose_event_del_en, reply_markup=keyboard)
            else:
                await bot.send_message(msg.from_user.id, messages.event_not_en)

        elif switch_text == "delete a mailing list":
            a = False
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM mail")
            result_set = cursor.fetchall()
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            for item in result_set:
                if item[0] == msg.from_user.id:
                    keyboard.add(item[1])
                    incoming_inst2.append(item[1])
                    a = True
            if a == True:
                state = dp.current_state(user=msg.from_user.id)
                await state.set_state(Delete.all()[1])
                await msg.reply(messages.choose_mail_del_en, reply_markup=keyboard)
            else:
                await bot.send_message(msg.from_user.id, messages.mail_not_en)

        elif switch_text == "back":
            await msg.reply(messages.settings_en, reply_markup=KeyBoards.setting_kb_en)

        # Изменение имени
        elif switch_text == "change the name":
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT chat_id, real_name FROM users")
            result_set = cursor.fetchall()
            for i in result_set:
                if i[0] == msg.from_user.id:
                    await bot.send_message(msg.from_user.id, f"Your past name: {i[1]}\n")
            conn.commit()
            conn.close()
            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(Change.all()[0])
            await bot.send_message(msg.from_user.id, "Enter your name 👇")

        # Изменение группы
        elif switch_text == "change a group":
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT chat_id, user_group, school FROM users")
            result_set = cursor.fetchall()
            for i in result_set:
                if i[0] == msg.from_user.id:
                    await bot.send_message(msg.from_user.id,
                                           f"Your institute: <b>{translate(i[2])}</b>\nYour group:"
                                           f" <b>{i[1]}</b>\n", parse_mode='HTML')
            conn.commit()
            conn.close()
            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(Register.all()[3])
            await msg.reply(messages.choose_inst_change_en, reply_markup=KeyBoards.institute_kb)

        elif switch_text == "view the group schedule":
            await msg.reply(messages.choose_inst_en, reply_markup=KeyBoards.institute_kb)
            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(ScheduleUser.all()[0])

        elif switch_text == "посмотреть расписание группы":
            await msg.reply(messages.choose_inst_en, reply_markup=KeyBoards.institute_kb)
            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(ScheduleUser.all()[0])
        elif switch_text == 'change the language':
            await msg.reply("Are you sure you want to change the language?", reply_markup=KeyBoards.yes_or_no_keyboard2_en)
            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(Change_Eu_Rus.all()[0])
        elif switch_text == "test":
            await msg.reply(f"{messages.greets_msg}")
        elif switch_text == "unload the entire database":
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT user_id FROM admins")
            result_set = cursor.fetchall()
            cursor.close()
            is_succeed = False
            for item in result_set:
                if item[0] == msg.from_user.id:
                    is_succeed = True
            if is_succeed:
                conn = sqlite3.connect('db.db')
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM users")
                result_set = cursor.fetchall()
                message = "<b>ID, имя пользователя и имя в боте и группа:</b>\n"
                for i in result_set:
                    message += str(i[0])
                    message += ", "
                    message += str(i[1])
                    message += ", "
                    message += str(i[2])
                    message += ", "
                    message += str(i[3])
                    message += "\n"
                    message += "\n"
                await bot.send_message(msg.from_user.id, message, parse_mode="HTML")
            else:
                await msg.reply(messages.not_admin_en, reply_markup=KeyBoards.menu_admin_kb_en)
        else:
            conn = sqlite3.connect('db.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT ru FROM users WHERE chat_id = '{msg.from_user.id}'")
            result_set = cursor.fetchall()
            cursor.close()
            is_ru = False
            if result_set[0][0] == "True":
                is_ru = True
            if is_ru == True:
                await bot.send_message(msg.from_user.id, messages.what)
            else:
                await bot.send_message(msg.from_user.id, messages.what_en)


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


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text(messages.what)
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)


if __name__ == "__main__":
    stopFlag = threading.Event()
    thread = MyThread(stopFlag)
    thread.start()
    stopFlag2 = threading.Event()
    thread2 = MyThread2(stopFlag2)
    thread2.start()
    stopFlag3 = threading.Event()
    thread3 = MyThread3(stopFlag3)
    thread3.start()
    stopFlag4 = threading.Event()
    thread4 = MyThread4(stopFlag4)
    thread4.start()
    executor.start_polling(dp, on_shutdown=shutdown, skip_updates=shutdown)
