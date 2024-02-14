from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from services.services import FillFrom, users
from keyboards.keyboards import inline_kb1, inline_kb2
from lexicon.lexicon_ru import LEXICON_RU

router = Router()

def profile(message: Message):
    return message.answer_photo(photo=users[message.from_user.id]['photo_id'],
                                   caption=f'Имя: {users[message.from_user.id]["name"]}\n'
                                            f'Возраст: {users[message.from_user.id]["age"]}\n'
                                            f'Пол: {users[message.from_user.id]["gender"]}\n'
                                            f'Город: {users[message.from_user.id]["city"]}\n'
                                            f'О себе: {users[message.from_user.id]["about_me"]}'
                                           )

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=LEXICON_RU['/start'])

@router.message(Command('help'))
async def help(message: Message):
    await message.answer(text=LEXICON_RU['/help'])

#Ждем корректный ввод имени
@router.callback_query(F.data.in_(['имя']))
@router.message(Command('profile'), StateFilter(default_state))
async def fill_profile(update, state: FSMContext):
    if update.from_user.id not in users:
        await update.answer(text=LEXICON_RU['имя'])
        await state.set_state(FillFrom.fill_name)
    else:
        if update.text == '/profile':
            await update.answer(text=LEXICON_RU['Есть анкета'])
        else:
            await update.message.answer(text=LEXICON_RU['имя'])
            await state.set_state(FillFrom.fill_name)

#Ждем корректный ввод возраста. Срабатывает, только если правильно ввести имя.
@router.callback_query(F.data.in_(['возраст']))
@router.message(StateFilter(FillFrom.fill_name), F.text.isalpha())
async def name_state(update, state: FSMContext):
    try:
        if update.data == 'возраст':
            await update.message.answer(text=LEXICON_RU['возраст'])
            await state.set_state(FillFrom.fill_age)
    except:
        if update.from_user.id not in users:
            await state.update_data(name=update.text)
            await update.answer(text=LEXICON_RU['возраст'])
            await state.set_state(FillFrom.fill_age)
        else:
            users[update.from_user.id]['name'] = update.text
            await state.clear()
            await update.answer(text=LEXICON_RU['изменение'])

#Неправильно введено имя
@router.message(StateFilter(FillFrom.fill_name))
async def incorrect_name(message: Message):
    await message.answer(LEXICON_RU['не имя'])

#Ждем корректный ввод пола, если правильно выбрали возраст.
@router.message(StateFilter(FillFrom.fill_age), lambda x: x.text.isdigit() and 18 <= int(x.text) <= 100)
async def gender_state(message: Message, state: FSMContext):
    if message.from_user.id not in users:
        await state.update_data(age=message.text)
        await message.answer(LEXICON_RU['пол'], reply_markup=inline_kb1)
        await state.set_state(FillFrom.fill_gender)
    else:
        users[message.from_user.id]['age'] = message.text
        await state.clear()
        await message.answer(text=LEXICON_RU['изменение'])

#Неправильно введен возраст
@router.message(StateFilter(FillFrom.fill_age))
async def incorrect_age(message: Message):
    await message.answer(LEXICON_RU['не возраст'])

#Ждем фото, если правильно выбрали пол
@router.callback_query(F.data.in_(['фото']))
@router.callback_query(StateFilter(FillFrom.fill_gender), F.data.in_(['М', 'Ж', 'оно']))
async def photo_state(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in users:
        await state.update_data(gender=callback.data)
        await callback.message.delete()
        await callback.message.answer(text=LEXICON_RU['фото'])
        await state.set_state(FillFrom.upload_photo)
    else:
        await callback.message.answer(text=LEXICON_RU['фото'])
        await state.set_state(FillFrom.upload_photo)

#Во время выбора пола отправлено что-то не то
@router.message(StateFilter(FillFrom.fill_gender))
async def incorrect_gender(message: Message):
    await message.answer(text=LEXICON_RU['не пол'])

#Ждем ввод города, если правильно отправлено фото
@router.callback_query(F.data.in_(['город']))
@router.message(StateFilter(FillFrom.upload_photo), F.photo[-1].as_('my_photo'))
async def city_state(update, state: FSMContext, my_photo: PhotoSize=None):
    try:
        if update.data == 'город':
            await update.message.answer(text=LEXICON_RU['город'])
            await state.set_state(FillFrom.fill_city)
    except:
        if update.from_user.id not in users:
            await state.update_data(photo_unique_id=my_photo.file_unique_id,
                                    photo_id=my_photo.file_id)
            await update.answer(LEXICON_RU['город'])
            await state.set_state(FillFrom.fill_city)
        else:
            users[update.from_user.id]['photo_id'] = my_photo.file_id
            users[update.from_user.id]['photo_unique_id'] = my_photo.file_unique_id
            await state.clear()
            await update.answer(text=LEXICON_RU['изменение'])

#Во время отправки фото отправлено что-то не то
@router.message(StateFilter(FillFrom.upload_photo))
async def incorrect_photo(message: Message):
    await message.answer(text=LEXICON_RU['не фото'])

#Ждем ввод о себе, если правильно введен город
@router.callback_query(F.data.in_(['о себе']))
@router.message(StateFilter(FillFrom.fill_city), F.text.isalpha())
async def about_me_state(update, state: FSMContext):
    try:
        if update.data == 'о себе':
            await update.message.answer(text=LEXICON_RU['о себе'])
            await state.set_state(FillFrom.fill_about_me)
    except:
        if update.from_user.id not in users:
            await state.update_data(city=update.text)
            await update.answer(text=LEXICON_RU['о себе'])
            await state.set_state(FillFrom.fill_about_me)
        else:
            users[update.from_user.id]['city'] = update.text
            await state.clear()
            await update.answer(text=LEXICON_RU['изменение'])

#Во время выбора города ввели что-то не то
@router.message(StateFilter(FillFrom.fill_city))
async def incorrect_photo(message: Message):
    await message.answer(text=LEXICON_RU['не город'])

#Все ввели верно, выходим из машины состояний
@router.message(StateFilter(FillFrom.fill_about_me), F.text)
async def create_profile(message: Message, state: FSMContext):
    if message.from_user.id not in users:
        await state.update_data(about_me=message.text)
        users[message.from_user.id] = await state.get_data()
        await state.clear()
        await message.answer(text=LEXICON_RU['анкета готова'])
    else:
        users[message.from_user.id]['city'] = message.text
        await state.clear()
        await message.answer(text=LEXICON_RU['изменение'])

#Что-то не то ввели в анкете о себе
@router.message(StateFilter(FillFrom.fill_about_me))
async def incorrect_about_me(message: Message):
    await message.answer(text=LEXICON_RU['не о себе'])

#Посмотреть анкету
@router.message(Command('getprofile'), StateFilter(default_state))
async def show_profile(message: Message):
    if message.from_user.id in users:
        await profile(message)
        await message.answer(text=LEXICON_RU['редактировать'])
    else:
        await message.answer(text=LEXICON_RU['нет анкеты'])

#Редактировать профиль
@router.message(Command('editProfile'))
async def edit_profile(message: Message):
    await message.answer(text='Что изменить?', reply_markup=inline_kb2)

