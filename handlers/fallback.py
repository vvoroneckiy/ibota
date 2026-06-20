import logging

from vkbottle.bot import Bot, Message

from utils.helpers import send_with_typing, get_main_keyboard

logger = logging.getLogger(__name__)


async def handle_fallback(message: Message) -> None:
    await send_with_typing(
        message,
        "Слушай, я твой свободный текст пока не вдупляю, пиши по-человечески или тыкай кнопки!",
        keyboard=get_main_keyboard(),
    )
