import logging
from typing import Optional

from vkbottle.bot import Bot, Message

from utils.constants import ADMIN_IDS
from utils.helpers import send_with_typing, get_main_keyboard
from database import get_all_users, set_ban

logger = logging.getLogger(__name__)


def is_admin_message(text: str) -> Optional[str]:
    if text.startswith("!рассылка") or text.startswith("!broadcast"):
        return "broadcast"
    if text.startswith("!бан") or text.startswith("!ban"):
        return "ban"
    return None


async def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def handle_admin(bot: Bot, message: Message) -> None:
    text = message.text.lower().strip()
    cmd = is_admin_message(text)

    if cmd == "broadcast":
        await handle_broadcast(bot, message)
    elif cmd == "ban":
        await handle_ban(bot, message)


async def handle_broadcast(bot: Bot, message: Message) -> None:
    if not await is_admin(message.from_id):
        await send_with_typing(
            message, "У тебя нет прав на эту команду.", keyboard=get_main_keyboard()
        )
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await send_with_typing(
            message,
            "Формат: !рассылка <текст>",
            keyboard=get_main_keyboard(),
        )
        return

    broadcast_text = parts[1]
    users = get_all_users()
    sent = 0

    for user_id, _ in users:
        try:
            await bot.api.messages.send(
                user_id=user_id,
                message=broadcast_text,
                random_id=0,
            )
            sent += 1
        except Exception:
            logger.exception(f"Failed to send broadcast to {user_id}")

    await send_with_typing(
        message,
        f"✅ Рассылка отправлена {sent}/{len(users)} пользователям.",
        keyboard=get_main_keyboard(),
    )


async def handle_ban(bot: Bot, message: Message) -> None:
    if not await is_admin(message.from_id):
        await send_with_typing(
            message, "У тебя нет прав на эту команду.", keyboard=get_main_keyboard()
        )
        return

    parts = message.text.split()
    if len(parts) < 2:
        await send_with_typing(
            message,
            "Формат: !бан <user_id>",
            keyboard=get_main_keyboard(),
        )
        return

    try:
        target_id = int(parts[1])
        set_ban(target_id, True)
        await send_with_typing(
            message,
            f"✅ Пользователь {target_id} забанен.",
            keyboard=get_main_keyboard(),
        )
    except ValueError:
        await send_with_typing(
            message,
            "❌ Некорректный ID пользователя.",
            keyboard=get_main_keyboard(),
        )
