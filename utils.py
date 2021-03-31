from aiogram.utils.helper import Helper, HelperMode, ListItem


class Register(Helper):
    mode = HelperMode.snake_case
    REGISTER_0 = ListItem()
    REGISTER_1 = ListItem()
    REGISTER_2 = ListItem()
    REGISTER_3 = ListItem()


class Schedule(Helper):
    mode = HelperMode.snake_case
    TEST_STATE_0 = ListItem()


class Change(Helper):
    mode = HelperMode.snake_case
    CHANGE_0 = ListItem()


class Pay(Helper):
    mode = HelperMode.snake_case
    PAY_DISTRIBUTOR = ListItem()
    PAY_DISTRIBUTOR2 = ListItem()


class AdminPanel(Helper):
    mode = HelperMode.snake_case
    ADMIN_0 = ListItem()
    ADMIN_1 = ListItem()
    ADMIN_2 = ListItem()
    ADMIN_3 = ListItem()