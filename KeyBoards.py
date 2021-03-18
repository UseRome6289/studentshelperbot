from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Регистрация")  # Первый
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Расписание").add("Профиль").add("Рассылки").\
                                                    add("Админ-панель").add("Чат").add("Настройки")  # Меню
mailing_lists_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")  # Рассылки
profile_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")  # Профиль
setting_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Назад").add("Рассылки"). \
                                                        add("Изменить информацию")  # Настройки
change_information_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Изменить имя").add("Изменить группу"). \
                                                                     add("Назад")  # Изменение информации о себе
mailing_lists_kb2 = ReplyKeyboardMarkup(resize_keyboard=True).add(
    "Изменить рассылки")  # Рассылки, в которых состоит пользователь
admin_panel = ReplyKeyboardMarkup(resize_keyboard=True).add(
    "Отправить рассылку").add("Меню")  # Отправление рассылок из админ-панели
chat_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    "Меню")  # Отправление рассылок из админ-панели
# Локация и контакт
markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
).add(
    KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
)
