import logging

from vkbottle.bot import Bot, Message

from utils.constants import STATS_TRIGGERS
from utils.helpers import send_with_typing, get_main_keyboard
from models.user import get_user_info, get_user_stats

logger = logging.getLogger(__name__)

STAT_LABELS = {
    "greeting": "👋 Приветствий",
    "compliment": "💬 Комплиментов",
    "fact": "🧠 Фактов",
    "challenge": "🎯 Квестов",
    "game_win": "🏆 Побед в играх",
}


def is_stats(text: str) -> bool:
    return any(t in text for t in STATS_TRIGGERS)


async def handle_stats(bot: Bot, message: Message) -> None:
    user_id = message.from_id

    user_info = await get_user_info(user_id)
    if not user_info:
        await send_with_typing(
            message,
            "Тебя нет в базе. Напиши 'Привет', чтобы зарегистрироваться!",
            keyboard=get_main_keyboard(),
        )
        return

    _, _, _, level, xp, _ = user_info
    xp_for_next = level * 100

    stats = await get_user_stats(user_id)

    lines = [
        f"📊 Твоя статистика:\n",
        f"🎯 Уровень: {level}",
        f"⭐ Опыт: {xp}/{xp_for_next}",
        "",
    ]

    for key, label in STAT_LABELS.items():
        count = stats.get(key, 0)
        lines.append(f"{label}: {count}")

    await send_with_typing(
        message, "\n".join(lines), keyboard=get_main_keyboard()
    )
