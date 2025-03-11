from aiogram.fsm.state import State, StatesGroup


class SendMessageStates(StatesGroup):
    crossing = State()
    template = State()
    # message_type = State()
