import logging
import random

from vkbottle.bot import Bot, Message

import phrases
from utils.constants import COMPLIMENT_TRIGGERS, XP_REWARDS
from utils.helpers import send_with_typing, get_main_keyboard
from models.user import reward_user

logger = logging.getLogger(__name__)


def is_compliment(text: str) -> bool:
    return any(t in text for t in COMPLIMENT_TRIGGERS)


async def handle_compliment(bot: Bot, message: Message) -> None:
    compliment = random.choice(phrases.COMPLIMENTS)

    new_level = await reward_user(message.from_id, "compliment", XP_REWARDS["compliment"])

    text = compliment
    if new_level:
        text += f"\n\n🎉 Ты достиг {new_level} уровня!"

    await send_with_typing(message, text, keyboard=get_main_keyboard())
