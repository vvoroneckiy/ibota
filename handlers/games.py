import logging
import random

from vkbottle.bot import Bot, Message

from utils.constants import XP_REWARDS, BOT_NAME
from utils.helpers import send_with_typing, get_main_keyboard
from models.user import reward_user

logger = logging.getLogger(__name__)

RPS_CHOICES = {"камень", "ножницы", "бумага"}
RPS_EMOJI = {"камень": "🪨", "ножницы": "✂️", "бумага": "📄"}
RPS_WINS = {"камень": "ножницы", "ножницы": "бумага", "бумага": "камень"}

TRIVIA = [
    {"q": "Сколько планет в Солнечной системе?", "a": "8"},
    {"q": "Какой газ мы выдыхаем?", "a": "Углекислый газ (CO₂)"},
    {"q": "Столица Франции?", "a": "Париж"},
    {"q": "Сколько дней в високосном году?", "a": "366"},
    {"q": "Как звали первого человека в космосе?", "a": "Юрий Гагарин"},
    {"q": "Сколько континентов на Земле?", "a": "6"},
    {"q": "Какое животное самое быстрое на суше?", "a": "Гепард"},
    {"q": "В какой стране изобрели бумагу?", "a": "В Китае"},
    {"q": "Сколько костей в теле человека?", "a": "206"},
    {"q": "Самый большой океан на Земле?", "a": "Тихий"},
]


def is_rps(text: str) -> bool:
    return text in RPS_CHOICES


def is_trivia(text: str) -> bool:
    return text in ("!викторина", "!quiz", "!игра", "!game", "!кнб", "!rps")


async def handle_rps(bot: Bot, message: Message) -> None:
    user_choice = message.text.lower().strip()
    bot_choice = random.choice(list(RPS_CHOICES))

    if user_choice == bot_choice:
        text = (
            f"{RPS_EMOJI[user_choice]} Ты: {user_choice}\n"
            f"{RPS_EMOJI[bot_choice]} {BOT_NAME}: {bot_choice}\n\n"
            f"🤝 Ничья!"
        )
    elif RPS_WINS[user_choice] == bot_choice:
        new_level = await reward_user(message.from_id, "game_win", XP_REWARDS["game_win"])
        text = (
            f"{RPS_EMOJI[user_choice]} Ты: {user_choice}\n"
            f"{RPS_EMOJI[bot_choice]} {BOT_NAME}: {bot_choice}\n\n"
            f"🎉 Ты победил! +{XP_REWARDS['game_win']} опыта"
        )
        if new_level:
            text += f"\n🎉 Ты достиг {new_level} уровня!"
    else:
        text = (
            f"{RPS_EMOJI[user_choice]} Ты: {user_choice}\n"
            f"{RPS_EMOJI[bot_choice]} {BOT_NAME}: {bot_choice}\n\n"
            f"😅 Я победил! Попробуй ещё раз."
        )

    await send_with_typing(message, text, keyboard=get_main_keyboard())


async def handle_trivia(bot: Bot, message: Message) -> None:
    q = random.choice(TRIVIA)
    await send_with_typing(
        message,
        f"❓ Вопрос:\n{q['q']}\n\n"
        f"💡 Ответ: ||{q['a']}||",
        keyboard=get_main_keyboard(),
        delay=2.0,
    )
