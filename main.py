import asyncio

from bot.app import bot, dp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sync import sync
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(sync, 'cron', minute='*/30')
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
