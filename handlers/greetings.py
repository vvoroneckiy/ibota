import logging
import random
from datetime import datetime

from vkbottle.bot import Bot, Message

import phrases
from utils.constants import GREETING_TRIGGERS, XP_REWARDS
from utils.helpers import send_with_typing, get_main_keyboard
from models.user import ensure_user, reward_user

logger = logging.getLogger(__name__)


def is_greeting(text: str) -> bool:
    return text in GREETING_TRIGGERS


async def handle_greeting(bot: Bot, message: Message) -> None:
    user_id = message.from_id
    user_info = await bot.api.users.get(user_ids=user_id)
    first_name = user_info[0].first_name

    await ensure_user(user_id, first_name)

    current_hour = datetime.now().hour
    if 0 <= current_hour < 5:
        greeting = random.choice(phrases.GREETINGS_NIGHT).format(name=first_name)
    else:
        greeting = random.choice(phrases.GREETINGS_DAY).format(name=first_name)

    new_level = await reward_user(user_id, "greeting", XP_REWARDS["greeting"])

    if new_level:
        greeting += f"\n\n🎉 Поздравляю! Ты достиг {new_level} уровня!"

    await send_with_typing(message, greeting, keyboard=get_main_keyboard())
