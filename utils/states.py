from aiogram.fsm.state import StatesGroup, State

class Description(StatesGroup):
    send = State()

class Files(StatesGroup):
    send = State()