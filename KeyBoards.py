from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Начало
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Регистрация")

# Добавил запланированные мероприятия для пользователя(По просьбе Никиты)
# Меню с админ-панелью
menu_admin_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Расписание").add("Админ-панель").add("Профиль")\
    .add("Рассылки")\
    .add("Посмотреть расписание другой группы").add("Запланированные мероприятия").add("Чат").add("Настройки")\
    .add("Поддержка разработчиков")

# Меню обычного пользователя
menu_user_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Расписание").add("Профиль").add("Рассылки")\
    .add("Посмотреть расписание другой группы").add("Запланированные мероприятия")\
    .add("Чат").add("Настройки").add("Поддержка разработчиков")

# Рассылки
mailing_lists_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Изменить рассылки").add("Меню")

# Профиль
profile_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

# Настройки
setting_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Рассылки"). \
                                                        add("Изменить информацию").add("Меню")

# Изменение информации о себе
change_information_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Изменить имя").\
    add("Изменить группу").add("Назад")

# Рассылки, в которых состоит пользователь
mailing_lists_kb2 = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

# Отправление рассылок из админ-панели
admin_panel = ReplyKeyboardMarkup(resize_keyboard=True).add("Отправить рассылку").add("Меню")

# Отправление рассылок из панели
chat_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

# Запланированные мероприятия
events_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Добавить мероприятие").add("Меню")

# Универсальная кнопка(просто в меню)
universal_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

# Выбор дня недели
day_of_the_week_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Понедельник").add("Вторник")\
                                                  .add("Среда").add("Четверг").add("Пятница").add("Суббота").add("Меню")
# Кнопки выбора института
institute_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("ИКИТ").add("ИУБП").add("ИФБиБТ").add("ИФиЯК").add("ВУЦ")\
        .add("ГИ").add("ИСИ").add("ИНиГ").add("ИАиД").add("ИГДГиГ").add("ИИФиРЭ").add("ИМиФИ").add("ИППС")\
        .add("ИФКСиТ").add("ИЦМиМ").add("ИЭиГ").add("ИГ").add("ИТиСУ").add("ИЭУиФ").add("ПИ").add("ЮИ")

# Курс
course_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("1 курс").add("2 курс").add("3 курс").add("4 курс")\
    .add("5 курс")

# Кнопки институтов
ikit_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("КИ20-17/1б (1 подгруппа)").add("КИ20-17/1б (2 подгруппа)")
gi_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("КИ20-02-5м")

# Поддержка разработчиков
developer_support_kb = ReplyKeyboardMarkup(resize_keyboard=True).add('Узнать команду разработчиков')\
    .add("Поддержать разработку телеграмм-бота").add("Меню")

# Локация и контакт
markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
).add(
    KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
)
