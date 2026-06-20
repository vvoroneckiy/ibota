from vkbottle.bot import Bot, Message

from handlers.greetings import is_greeting, handle_greeting
from handlers.compliments import is_compliment, handle_compliment
from handlers.facts import is_fact, handle_fact
from handlers.challenges import is_challenge, handle_challenge
from handlers.stats import is_stats, handle_stats
from handlers.admin import is_admin_message, handle_admin
from handlers.games import is_rps, handle_rps, is_trivia, handle_trivia
from handlers.weather import is_weather, handle_weather, handle_weather_city_input
from utils.states import WeatherState


async def route_message(bot: Bot, message: Message) -> bool:
    text = message.text.lower().strip()

    state = await bot.state_dispenser.get(message.from_id)
    if state is not None and state.state == WeatherState.AWAITING_CITY:
        await handle_weather_city_input(bot, message)
        return True

    if is_greeting(text):
        await handle_greeting(bot, message)
        return True

    if is_admin_message(text):
        await handle_admin(bot, message)
        return True

    if is_compliment(text):
        await handle_compliment(bot, message)
        return True

    if is_fact(text):
        await handle_fact(bot, message)
        return True

    if is_challenge(text):
        await handle_challenge(bot, message)
        return True

    if is_stats(text):
        await handle_stats(bot, message)
        return True

    if is_rps(text):
        await handle_rps(bot, message)
        return True

    if is_trivia(text):
        await handle_trivia(bot, message)
        return True

    if is_weather(text):
        await handle_weather(bot, message)
        return True

    return False
