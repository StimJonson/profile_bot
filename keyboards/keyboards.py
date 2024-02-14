from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lexicon.lexicon_ru import LEXICON_RU

btn1 = InlineKeyboardButton(text=LEXICON_RU['мужской'], callback_data='М')
btn2 = InlineKeyboardButton(text=LEXICON_RU['женский'], callback_data='Ж')
btn3 = InlineKeyboardButton(text=LEXICON_RU['Европа'], callback_data='оно')

inline_kb1 = InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2, btn3]])

bt1 = InlineKeyboardButton(text=LEXICON_RU['ред имя'], callback_data='имя')
bt2 = InlineKeyboardButton(text=LEXICON_RU['ред возраст'], callback_data='возраст')
bt3 = InlineKeyboardButton(text=LEXICON_RU['ред город'], callback_data='город')
bt4 = InlineKeyboardButton(text=LEXICON_RU['ред фото'], callback_data='фото')
bt5 = InlineKeyboardButton(text=LEXICON_RU['ред о себе'], callback_data='о себе')

inline_kb2 = InlineKeyboardMarkup(inline_keyboard=[[bt1], [bt2], [bt3], [bt4], [bt5]])