from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Начало
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Регистрация")

# Добавил запланированные мероприятия для пользователя(По просьбе Никиты)
# Меню с админ-панелью
menu_admin_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Расписание").add("Профиль").add("Рассылки").\
                         add("Запланированные мероприятия").add("Чат").add("Настройки").add("Поддержка разработчиков")

# Меню обычного пользователя
menu_user_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Расписание").add("Профиль").add("Рассылки").\
       add("Запланированные мероприятия").add("Админ-панель").add("Чат").add("Настройки").add("Поддержка разработчиков")

# Рассылки
mailing_lists_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

# Профиль
profile_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

# Настройки
setting_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Рассылки"). \
                                                        add("Изменить информацию").add("Меню")

# Изменение информации о себе
change_information_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Изменить имя").add("Изменить группу"). \
                                                                add("Назад")

# Рассылки, в которых состоит пользователь
mailing_lists_kb2 = ReplyKeyboardMarkup(resize_keyboard=True).add("Изменить рассылки").add("Меню")

# Отправление рассылок из админ-панели
admin_panel = ReplyKeyboardMarkup(resize_keyboard=True).add("Отправить рассылку").add("Меню")

# Отправление рассылок из админ-панели
chat_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

# Запланированные мероприятия
events_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Добавить мероприятие").add("Меню")

# Универсальная кнопка(просто в меню)
universal_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

# Локация и контакт
markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
).add(
    KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
)
