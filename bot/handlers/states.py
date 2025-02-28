from aiogram.fsm.state import State, StatesGroup


class AppealStates(StatesGroup):
    appeal = State()


class NotificationStates(StatesGroup):
    notification_type = State()
