import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import *

from data import database as db
from config_reader import config
from handlers import setting_time, bot_messages, weather

async def main():
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    await db.db_start()
    asyncio.create_task(weather.scheduler(bot))

    dp.include_routers(
        setting_time.router,
        bot_messages.router
    )

    await bot.delete_webhook(drop_pending_updates= True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())