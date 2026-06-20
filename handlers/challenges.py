import logging
import random

from vkbottle.bot import Bot, Message

import phrases
from utils.constants import CHALLENGE_TRIGGERS, XP_REWARDS
from utils.helpers import send_with_typing, get_main_keyboard
from models.user import reward_user

logger = logging.getLogger(__name__)


def is_challenge(text: str) -> bool:
    return any(t in text for t in CHALLENGE_TRIGGERS)


async def handle_challenge(bot: Bot, message: Message) -> None:
    await send_with_typing(
        message,
        "Так-так-так... Мои шестерёнки крутятся, генератор бреда запущен! Лови задание:",
    )

    challenge = random.choice(phrases.CHALLENGES)

    new_level = await reward_user(message.from_id, "challenge", XP_REWARDS["challenge"])

    text = challenge
    if new_level:
        text += f"\n\n🎉 Ты достиг {new_level} уровня!"

    await send_with_typing(
        message, text, keyboard=get_main_keyboard(), delay=1.2
    )
