import sqlite3
import requests
import re

from aiogram.types import ReplyKeyboardMarkup

from messages import help_message
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import TOKEN


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

@dp.message_handler(commands='start')
async def process_start_command(message: types.Message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users(chat_id, name) values ({message.from_user.id}, '{message.from_user.username}')")
    conn.commit()
    conn.close()
    await message.reply(f'Доброго времени суток!, {message.from_user.username}.\n'
                        '\n Это наш StudentHelperBot, здесь всегда можно узнать актуальное расписание, поставить'
                        'напоминания, подписаться на рассылки: чат группы, сообщения от преподавателей, у нас есть свои'
                        'PevCoin\'ы (валюта в разработке)\n\nПройдем регистрацию?)')



@dp.message_handler(commands='help')
async def process_help_command(message: types.Message):
    await message.reply(help_message)


@dp.message_handler(content_types=["text"])
async def handler_message(msg: types.Message):
    switch_text = msg.text.lower()
    if msg.text == "расписание":
        timetable_message = ""
        current_week = "0"
        url = 'https://edu.sfu-kras.ru/timetable'
        response = requests.get(url).text
        match = re.search(r'Идёт\s\w{8}\sнеделя', response)
        if match:
            timetable_message += "Сейчас идёт <b>нечётная</b> неделя\n"
            current_week = "1"
        else:
            timetable_message += "Сейчас идёт <b>чётная</b> неделя\n"
            current_week = "2"
        url = 'http://edu.sfu-kras.ru/api/timetable/get?target=КИ20-17/1б (2 подгруппа)'
        response = requests.get(url).json()
        for item in response["timetable"]:
            if item["week"] == current_week:
                timetable_message += f"\n{item['day'].replace('1','<b>Понедельник</b>').replace('2', '<b>Вторник</b>').replace('3', '<b>Среда</b>').replace('4','<b>Четверг</b>').replace('5', '<b>Пятница</b>').replace('6','<b>Суббота</b>')}" \
                                     f"\n{item['time']}\n{item['subject']}\n{item['type']}\n" \
                                     f"{item['teacher']}\n{item['place']}\n"
        await msg.reply(timetable_message, parse_mode="HTML")


if __name__ == "__main__":
    executor.start_polling(dp, on_shutdown=shutdown)
