import asyncio
import logging
from functools import lru_cache

from vkbottle import Keyboard, Text, KeyboardButtonColor
from vkbottle.bot import Message

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_main_keyboard() -> str:
    return (
        Keyboard(one_time=False)
        .add(Text("Выдай комплимент"), color=KeyboardButtonColor.SECONDARY)
        .add(Text("Угарный факт"), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text("Погода"), color=KeyboardButtonColor.SECONDARY)
        .add(Text("Квест / Подгон на сегодня"), color=KeyboardButtonColor.PRIMARY)
    ).get_json()


async def send_with_typing(
    message: Message,
    text: str,
    keyboard: str = None,
    delay: float = 1.0,
) -> None:
    try:
        await message.ctx_api.messages.set_activity(
            type="typing",
            peer_id=message.peer_id,
        )
        await asyncio.sleep(delay)
        await message.answer(text, keyboard=keyboard)
    except Exception:
        logger.exception("Failed to send message")
