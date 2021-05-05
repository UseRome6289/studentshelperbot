from aiogram.utils.helper import Helper, HelperMode, ListItem


class Register(Helper):
    mode = HelperMode.snake_case
    REGISTER_0 = ListItem()
    REGISTER_1 = ListItem()
    REGISTER_2 = ListItem()
    REGISTER_3 = ListItem()
    REGISTER_4 = ListItem()
    REGISTER_5 = ListItem()


class Change(Helper):
    mode = HelperMode.snake_case
    CHANGE_0 = ListItem()


class Pay(Helper):
    mode = HelperMode.snake_case
    PAY_DISTRIBUTOR = ListItem()
    PAY_DISTRIBUTOR2 = ListItem()
    PAY_DISTRIBUTOR3 = ListItem()


class AdminPanel(Helper):
    mode = HelperMode.snake_case
    ADMIN_0 = ListItem()
    ADMIN_1 = ListItem()
    ADMIN_2 = ListItem()
    ADMIN_3 = ListItem()
    ADMIN_4 = ListItem()
    ADMIN_5 = ListItem()
    ADMIN_6 = ListItem()
    ADMIN_7 = ListItem()
    ADMIN_8 = ListItem()
    ADMIN_9 = ListItem()


class ScheduleUser(Helper):
    mode = HelperMode.snake_case
    SCHEDULE_USER_0 = ListItem()
    SCHEDULE_USER_1 = ListItem()
    SCHEDULE_USER_2 = ListItem()
    SCHEDULE_USER_3 = ListItem()
    SCHEDULE_USER_4 = ListItem()


class Schedule(Helper):
    mode = HelperMode.snake_case
    SCHEDULE_0 = ListItem()


class CheckSchedule(Helper):
    mode = HelperMode.snake_case
    SCH_0 = ListItem()


class Events(Helper):
    mode = HelperMode.snake_case
    EVENTS_USER_0 = ListItem()
    EVENTS_USER_1 = ListItem()


class Delete(Helper):
    mode = HelperMode.snake_case
    DELETE_EVENTS_0 = ListItem()
    DELETE_EVENTS_1 = ListItem()
    DELETE_EVENTS_2 = ListItem()
    DELETE_EVENTS_3 = ListItem()
