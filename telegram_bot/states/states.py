from aiogram.fsm.state import StatesGroup, State


class AnonMessageStates(StatesGroup):
    user_id = State()
    message = State()

    # reciever part
    answer = State()
    report = State()


