from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()

class FillFrom(StatesGroup):
    fill_name = State()
    fill_age = State()
    fill_gender = State()
    upload_photo = State()
    fill_city = State()
    fill_about_me = State()

users: dict[int, dict[str, str | int | bool]] = {}