from aiogram.fsm.state import StatesGroup, State


class AnonMessageStates(StatesGroup):
    user_id = State()
    text = State()
