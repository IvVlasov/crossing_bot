from aiogram.fsm.state import State, StatesGroup


class SendMessageStates(StatesGroup):
    crossing = State()
    # message_type = State()
