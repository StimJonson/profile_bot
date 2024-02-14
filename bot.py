import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import user_handlers, other_handlers
from keyboards.set_menu import start_bot
from config_data.config import config

bot_token = config.tg_bot.token
admin_ids = config.tg_bot.admin_ids

async def stop_bot(bot: Bot):
    await bot.send_message(admin_ids[0], 'Бот остановлен')

logger = logging.getLogger('test_bot')
logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

async def start():
    bot = Bot(token=bot_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    dp.startup.register(start_bot)
    logger.info('Starting Bot')
    dp.shutdown.register(stop_bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())