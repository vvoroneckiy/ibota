import logging
import os
import sys
from datetime import datetime

import aiohttp
from dotenv import load_dotenv
from vkbottle.bot import Bot, Message
from vkbottle.http import AiohttpClient

from database import init_db
from handlers.router import route_message
from handlers.admin import is_admin_message
from models.user import check_banned
from utils.constants import BOT_NAME

load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("\n[КРИТИЧЕСКАЯ ОШИБКА] Токен не найден в системе!")
    print("Проверь, что в папке 'ibota' создан файл с именем '.env' (БЕЗ .txt на конце).")
    print("Внутри файла должна быть строчка: TOKEN=твой_токен\n")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"logs/bot_{datetime.now().strftime('%Y%m%d')}.log"),
    ],
)
logger = logging.getLogger(__name__)

init_db()
logger.info("Database initialized")

bot = Bot(token=TOKEN)
logger.info(f"Bot '{BOT_NAME}' created")


async def patch_ssl_on_startup() -> None:
    connector = aiohttp.TCPConnector(ssl=False)
    session = aiohttp.ClientSession(connector=connector)
    bot.api.http_client = AiohttpClient(session=session)
    logger.info("SSL verification disabled for aiohttp")


bot.on_startup.append(patch_ssl_on_startup())


@bot.on.message()
async def router(message: Message) -> None:
    user_id = message.from_id

    if user_id > 0 and await check_banned(user_id):
        logger.warning(f"Banned user {user_id} tried to interact")
        return

    handled = await route_message(bot, message)
    if not handled:
        from handlers.fallback import handle_fallback
        await handle_fallback(message)


if __name__ == "__main__":
    print(f"=== {BOT_NAME} ЗАПУЩЕН ===")
    logger.info("Bot started")
    bot.run()
