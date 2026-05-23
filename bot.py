import asyncio
import random
import ssl
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from vkbottle import Keyboard, Text, KeyboardButtonColor
from vkbottle.bot import Bot, Message

import phrases

load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("\n[КРИТИЧЕСКАЯ ОШИБКА] Токен не найден в системе!")
    print("Проверь, что в папке 'ibota' создан файл с именем '.env' (БЕЗ .txt на конце).")
    print("Внутри файла должна быть строчка: VK_TOKEN=твой_токен\n")
    sys.exit(1)

ssl._create_default_https_context = ssl._create_unverified_context

bot = Bot(token=TOKEN)

async def send_with_typing(message: Message, text: str, keyboard: Keyboard = None, delay: float = 1.0):
    await bot.api.messages.set_activity(type="typing", peer_id=message.peer_id)
    await asyncio.sleep(delay)
    await message.answer(text, keyboard=keyboard)

def get_main_keyboard():
    return (Keyboard(one_time=False)
            .add(Text("Выдай комплимент"), color=KeyboardButtonColor.SECONDARY)
            .add(Text("Угарный факт"), color=KeyboardButtonColor.SECONDARY)
            .row()
            .add(Text("Квест / Подгон на сегодня"), color=KeyboardButtonColor.PRIMARY)
            ).get_json()

@bot.on.message()
async def main_handler(message: Message):
    user_id = message.from_id
    user_info = await bot.api.users.get(user_ids=user_id)
    first_name = user_info[0].first_name
    
    raw_text = message.text.lower().strip()

    if raw_text in ["начать", "привет", "прив", "хай", "ку", "здорова", "салют"]:
        current_hour = datetime.now().hour
        
        if 0 <= current_hour < 5:
            greeting = random.choice(phrases.GREETINGS_NIGHT).format(name=first_name)
        else:
            greeting = random.choice(phrases.GREETINGS_DAY).format(name=first_name)
            
        await send_with_typing(message, greeting, keyboard=get_main_keyboard())
        return

    if "комплимент" in raw_text:
        await send_with_typing(message, random.choice(phrases.COMPLIMENTS))
        return

    if "факт" in raw_text:
        await send_with_typing(message, random.choice(phrases.FACTS))
        return

    if "квест" in raw_text or "подгон" in raw_text:
        await send_with_typing(message, "Так-так-так... Мои шестерёнки крутятся, генератор бреда запущен! Лови задание:")
        await send_with_typing(message, random.choice(phrases.CHALLENGES), keyboard=get_main_keyboard(), delay=1.2)
        return

    await send_with_typing(message, "Слушай, я твой свободный текст пока не вдупляю, пиши по-человечески или тыкай кнопки!", keyboard=get_main_keyboard())

if __name__ == "__main__":
    print("=== БОТ ИЗУЧИЛ 100 ФРАЗ, ЗАГРУЗИЛ .ENV И УСПЕШНО ЗАПУСТИЛСЯ ===")
    bot.run_forever()