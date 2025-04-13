from bot.services.mailing_service import MailingService
import asyncio
from datetime import datetime
from bot.models import NotificationType
import logging

logger = logging.getLogger(__name__)


async def sync():
    logger.info("Syncing")
    now = datetime.now()
    mailing_service = MailingService()

    if now.hour == 6 and now.minute == 0:
        await mailing_service.send_notification(NotificationType.SIX_HOURS)

    if now.hour == 17 and now.minute == 0:
        await mailing_service.send_notification(NotificationType.SEVENTEEN_HOURS)

    if now.hour > 5:
        await mailing_service.check_weather()


if __name__ == "__main__":
    asyncio.run(sync())
