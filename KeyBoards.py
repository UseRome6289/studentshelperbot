from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Начало
select_RU_EN = ReplyKeyboardMarkup(resize_keyboard=True).add("EN🇬🇧").add("RU🇷🇺")
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Я студент").add("Я преподаватель")
greet_kb2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Я студент")
greet_kb_en = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("I'm a student").add("I'm a teacher")
greet_kb2_en = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("I'm a student")
# Меню с админ-панелью
menu_admin_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Расписание").add("Админ-панель").add("Профиль") \
    .add("Рассылки") \
    .add("Посмотреть расписание группы или преподавателя").add("Запланированные мероприятия")\
    .add("Настройки") \
    .add("Выгрузить всю базу данных")

# Меню обычного пользователя
menu_user_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Расписание").add("Профиль").add("Рассылки") \
    .add("Посмотреть расписание группы или преподавателя").add("Запланированные мероприятия")\
     \
    .add("Настройки")
schedule_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Посмотреть расписание другой группы")\
    .add("Посмотреть расписание преподавателя").add("Меню")

# Рассылки
mailing_lists_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Удалить рассылку").add("Меню")

# Профиль
profile_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

# Настройки
setting_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Рассылки").add('Запланированные мероприятия'). \
    add("Изменить информацию").add('Поменять язык').add("Меню")

# Изменение информации о себе
change_information_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Изменить имя"). \
    add("Изменить группу").add("Назад")
change_information_kb2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Поменять преподавателя") \
    .add("Назад")
# Рассылки, в которых состоит пользователь
mailing_lists_kb2 = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

# Отправление рассылок из админ-панели
admin_panel = ReplyKeyboardMarkup(resize_keyboard=True).add("Отправить рассылку") \
    .add('Отправить рассылку всем пользователям').add("Добавить преподавателя").add("Меню")
admin_panel_teacher = ReplyKeyboardMarkup(resize_keyboard=True).add("Отправить рассылку") \
    .add("Меню")
# Запланированные мероприятия
events_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Добавить мероприятие").add("Удалить мероприятие").add("Меню")

# Универсальная кнопка(просто в меню)
universal_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

# Выбор дня недели
day_of_the_week_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("Понедельник").add("Вторник") \
    .add("Среда").add("Четверг").add("Пятница").add("Суббота") \
    .add('Посмотреть расписание на след. неделю').add("Меню")
day_of_the_week_kb2 = ReplyKeyboardMarkup(resize_keyboard=True).add("Понедельник").add("Вторник") \
    .add("Среда").add("Четверг").add("Пятница").add("Суббота") \
    .add('Посмотреть расписание нынешней недели').add("Меню")
# Кнопки выбора института
institute_kb = ReplyKeyboardMarkup(resize_keyboard=True).add('ИКИТ').add('ВИИ').add('ГИ').add('ИСИ').add('ИАиД') \
    .add('ИГ').add('ИГДГиГ').add('ИИФиРЭ').add('ИМиФИ').add('ИНиГ').add('ИППС').add('ИТиСУ').add('ИУБП').add('ИФКСиТ') \
    .add('ИФиЯК').add('ИЦМиМ').add('ИЭиГ').add('ИЭГУиФ').add('ПИ').add('ЮИ').add('ИФБиБТ')

# Кнопки институтов
ikit_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("КИ20-17/1б (1 подгруппа)").add("КИ20-17/1б (2 подгруппа)")
gi_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("КИ20-02-5м")

# Поддержка разработчиков
developer_support_kb = ReplyKeyboardMarkup(resize_keyboard=True).add('Узнать команду разработчиков') \
    .add("Поддержать разработку телеграмм-бота").add("Меню")

developer_support_kb2 = ReplyKeyboardMarkup(resize_keyboard=True).add('Поддержать разработчиков 100 рублей') \
    .add("Поддержать разработчиков 250 рублей").add("Поддержать разработчиков 500 рублей") \
    .add("Поддержать разработчиков 1000 рублей").add('Поддержать разработчиков другой суммой').add('Меню')

# Локация и контакт
markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
).add(
    KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
)
return_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add("Меню")

yes_or_no_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add("Да").add("Изменить").add("Меню")
yes_or_no_keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True).add("Да").add("Меню")
time_kb = ReplyKeyboardMarkup(resize_keyboard=True).add("1 час").add('2 часа').add('3 часа').add('4 часа') \
    .add('5 часов').add("6 часов").add("12 часов").add('18 часов').add('24 часа').add('2 дня').add('3 дня') \
    .add('Неделя').add('Меню')
time_kb2 = ReplyKeyboardMarkup(resize_keyboard=True).add('Без таймера').add("1 час").add('2 часа').add('3 часа').add(
    '4 часа') \
    .add('5 часов').add("6 часов").add("12 часов").add('18 часов').add('24 часа').add('2 дня').add('3 дня') \
    .add('Неделя').add('Меню')


#english
# Меню с админ-панелью
schedule_kb_en = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("View the group schedule")\
    .add("View the teacher's schedule").add("Menu")
menu_admin_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Schedule").add("Admin Panel").add("Profile") \
    .add("Mailing lists") \
    .add("Planned events").add("View the group schedule or teacher's schedule").add("Settings") \
    .add("Unload the entire database")

# Меню обычного пользователя
menu_user_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Schedule").add("Profile").add("Mailing lists") \
    .add("Planned events").add("View the group schedule or teacher's schedule") \
    .add("Settings")

# Рассылки
mailing_lists_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Delete a mailing list").add("Menu")

# Профиль
profile_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Menu")

# Настройки
setting_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Mailing lists").add('Planned events'). \
    add("Change information").add("Change the language").add("Menu")

# Изменение информации о себе
change_information_kb_en = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Change the name"). \
    add("Change a group").add("Back")
change_information_kb2_en = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Change the teacher") \
    .add("Back")
# Рассылки, в которых состоит пользователь
mailing_lists_kb2_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Menu")

# Отправление рассылок из админ-панели
admin_panel_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Send a newsletter") \
    .add('Send a newsletter to all users').add("Add a teacher").add("Menu")
admin_panel_teacher_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Send a newsletter") \
    .add("Menu")
# Запланированные мероприятия
events_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Add an event").add("Delete an event").add("Menu")

# Универсальная кнопка(просто в меню)
universal_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Menu")

# Выбор дня недели
day_of_the_week_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Monday").add("Tuesday") \
    .add("Wednesday").add("Thursday").add("Friday").add("Saturday") \
    .add("View next week's schedule").add("Menu")
day_of_the_week_kb2_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Monday").add("Tuesday") \
    .add("Wednesday").add("Thursday").add("Friday").add("Saturday") \
    .add("View the schedule for the current week").add("Menu")
return_keyboard_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Menu")
yes_or_no_keyboard_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Yes").add("To change").add("Menu")
yes_or_no_keyboard2_en = ReplyKeyboardMarkup(resize_keyboard=True).add("Yes").add("Menu")
time_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add("1 hour").add('2 hours').add('3 hours').add('4 hours') \
    .add('5 hours').add("6 hours").add("12 hours").add('18 hours').add('24 hours').add('2 days').add('3 days') \
    .add('A week').add('Menu')
time_kb2_en = ReplyKeyboardMarkup(resize_keyboard=True).add('Without a timer').add("1 hour").add('2 hours').add('3 hours').add('4 hours') \
    .add('5 hours').add("6 hours").add("12 hours").add('18 hours').add('24 hours').add('2 days').add('3 days') \
    .add('A week').add('Menu')

alphabet = {"а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у",
            "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4',
            '5', '6', '7', '8', '9', '0', '(', ')', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '.', ',', 'А', 'Б', 'В', 'Г', 'Д', 'Е',
            'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ',
            'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', '-', '/', ' ', '', "!"}
