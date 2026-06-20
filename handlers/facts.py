import logging
import random

from vkbottle.bot import Bot, Message

import phrases
from utils.constants import FACT_TRIGGERS, XP_REWARDS
from utils.helpers import send_with_typing, get_main_keyboard
from models.user import reward_user

logger = logging.getLogger(__name__)


def is_fact(text: str) -> bool:
    return any(t in text for t in FACT_TRIGGERS)


async def handle_fact(bot: Bot, message: Message) -> None:
    fact = random.choice(phrases.FACTS)

    new_level = await reward_user(message.from_id, "fact", XP_REWARDS["fact"])

    text = fact
    if new_level:
        text += f"\n\n🎉 Ты достиг {new_level} уровня!"

    await send_with_typing(message, text, keyboard=get_main_keyboard())
