import logging

import aiohttp
from vkbottle.bot import Bot, Message

from utils.constants import WEATHER_TRIGGERS
from utils.helpers import send_with_typing, get_main_keyboard
from utils.states import WeatherState

logger = logging.getLogger(__name__)

WMO_CODES = {
    0: "☀️ Ясно",
    1: "🌤 Малооблачно",
    2: "⛅ Переменная облачность",
    3: "☁️ Пасмурно",
    45: "🌫 Туман",
    48: "🌫 Иней",
    51: "🌦 Легкая морось",
    53: "🌦 Морось",
    55: "🌧 Сильная морось",
    61: "🌦 Небольшой дождь",
    63: "🌧 Дождь",
    65: "🌧 Сильный дождь",
    71: "🌨 Небольшой снег",
    73: "🌨 Снег",
    75: "🌨 Сильный снег",
    80: "🌦 Ливень",
    81: "🌧 Сильный ливень",
    82: "🌧 Шквальный дождь",
    95: "⛈ Гроза",
    96: "⛈ Гроза с градом",
    99: "⛈ Сильная гроза с градом",
}

API_URL = "https://api.open-meteo.com/v1/forecast"
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"


def is_weather(text: str) -> bool:
    cmd = text.split()[0] if text else ""
    return cmd in WEATHER_TRIGGERS


def extract_city(text: str) -> str:
    parts = text.split(maxsplit=1)
    if len(parts) > 1:
        return parts[1].strip()
    return ""


async def get_user_city(bot: Bot, user_id: int) -> str | None:
    try:
        user_info = await bot.api.users.get(user_ids=user_id, fields="city")
        city_data = user_info[0].city
        if city_data:
            return city_data.title
    except Exception:
        logger.exception("Failed to get user city")
    return None


async def geocode_city(city: str) -> tuple[float, float, str] | None:
    try:
        async with aiohttp.ClientSession() as session:
            params = {"name": city, "count": 1, "language": "ru", "format": "json"}
            async with session.get(GEO_URL, params=params) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                results = data.get("results")
                if not results:
                    return None
                r = results[0]
                lat = r["latitude"]
                lon = r["longitude"]
                name = r.get("name", city)
                country = r.get("country", "")
                return lat, lon, f"{name}, {country}" if country else name
    except Exception:
        logger.exception("Geocode error")
        return None


async def fetch_weather(lat: float, lon: float) -> dict | None:
    try:
        async with aiohttp.ClientSession() as session:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,precipitation",
                "timezone": "auto",
            }
            async with session.get(API_URL, params=params) as resp:
                if resp.status != 200:
                    return None
                return await resp.json()
    except Exception:
        logger.exception("Weather fetch error")
        return None


async def show_weather(
    bot: Bot, message: Message, city: str
) -> None:
    coords = await geocode_city(city)
    if coords is not None:
        lat, lon, display_name = coords
        data = await fetch_weather(lat, lon)
        if data and "current" in data:
            c = data["current"]
            temp = c["temperature_2m"]
            feels = c["apparent_temperature"]
            humidity = c["relative_humidity_2m"]
            wind = c["wind_speed_10m"]
            precip = c["precipitation"]
            code = c["weather_code"]
            weather_desc = WMO_CODES.get(code, f"Код {code}")

            text = (
                f"🌍 {display_name}\n\n"
                f"{weather_desc}\n"
                f"🌡 {temp}°C (ощущается как {feels}°C)\n"
                f"💧 Влажность: {humidity}%\n"
                f"💨 Ветер: {wind} км/ч\n"
                f"🌧 Осадки: {precip} мм"
            )
            await send_with_typing(message, text, keyboard=get_main_keyboard())
            return

    await send_with_typing(
        message,
        f"Не нашёл город '{city}'. Попробуй по-другому.",
        keyboard=get_main_keyboard(),
    )


async def handle_weather_city_input(bot: Bot, message: Message) -> None:
    city = message.text.strip()
    await bot.state_dispenser.delete(message.from_id)
    await show_weather(bot, message, city)


async def handle_weather(bot: Bot, message: Message) -> None:
    city = extract_city(message.text)

    if not city:
        city = await get_user_city(bot, message.from_id)

    if city:
        await show_weather(bot, message, city)
        return

    await bot.state_dispenser.set(message.from_id, WeatherState.AWAITING_CITY)
    await send_with_typing(
        message,
        "В каком городе смотрим погоду? Напиши название.",
        keyboard=get_main_keyboard(),
    )
