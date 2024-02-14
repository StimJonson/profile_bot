from lexicon.lexicon_ru import LEXICON_START_MENU_RU
from aiogram import Bot
from aiogram.types import BotCommand
from config_data.config import config
import logging

async def start_bot(bot: Bot):
    main_menu_commands = [BotCommand(command=command, description=description)
                                     for command, description in LEXICON_START_MENU_RU.items()]
    await bot.set_my_commands(main_menu_commands)
    await bot.send_message(config.tg_bot.admin_ids[0], 'Бот запущен')