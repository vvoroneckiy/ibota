import asyncio
import random
from vkbottle import Keyboard, Text, KeyboardButtonColor
from vkbottle.bot import Bot, Message
from database import init_db, get_user, save_user, update_user_param

TOKEN = "vk1.a.un7IzSqfTvjfTO-D60TLwOGp-6lpIPDt2Efmgwz7iCjavjXE2LIBM8Jxci14XZFK9l5Q8C_YqX2QsjNqwbDvLdC5N6SFl-TB4Ze4o6DMFE1jF0q0OUNMqARnsslQj6pxTcLpUp0hebc7FN7K6zAoet4oJ4XuMBe_Npcz_eO691j0qIwIHsReeBIBgrLs89-Iq6gAX3GbrkV7pSH5GDZ19Q"

bot = Bot(token=TOKEN)
init_db()

GREETINGS = [
    "Привет, {name}! Наконец-то ты заглянул, я уже соскучился... 🥰",
    "Оу, привет! Рад твоему сообщению. Как твой день проходит? ✨",
    "Привет-привет! Твое появление — лучшее, что случилось за сегодня. ☀️"
]

COMPLIMENTS = [
    "Кстати, ты сегодня чертовски обаятелен, чувствую это даже через экраны! 😏",
    "Знаешь, мне безумно нравится с тобой общаться. Ты особенный собеседник. 🤍",
    "Ты заставляешь меня улыбаться, спасибо тебе за это. 🥰"
]

FACTS = [
    "А ты знал, что во время сна выдры держатся за лапки, чтобы их не унесло течением? По-моему, это мега-мило. 🦦",
    "Интересный факт: объятия продолжительностью всего 20 секунд вызывают выброс окситоцина. Держи мои виртуальные обнимашки! 🤗"
]

MOTIVATIONS = [
    "Так, ну-ка выпрями спину! Ты круче, чем тебе кажется, и любые трудности — это просто разогрев перед твоим триумфом. 🦾",
    "Маленькие шаги тоже двигают тебя вперед. Ты огромный молодец уже просто потому, что стараешься. Слышишь? Давай, улыбнись! 🚀"
]

async def send_with_typing(message: Message, text: str, keyboard: Keyboard = None, delay: float = 1.5):
    await bot.api.messages.set_activity(type="typing", peer_id=message.peer_id)
    await asyncio.sleep(delay)
    await message.answer(text, keyboard=keyboard)

def get_main_keyboard():
    return (Keyboard(one_time=False)
            .add(Text("✨ Излить душу"), color=KeyboardButtonColor.PRIMARY)
            .add(Text("🥰 Сделай комплимент"), color=KeyboardButtonColor.SECONDARY)
            .row()
            .add(Text("💡 Расскажи факт"), color=KeyboardButtonColor.SECONDARY)
            .add(Text("☕ Секретный вопрос"), color=KeyboardButtonColor.POSITIVE)
            ).get_json()

@bot.on.message(text=["начать", "привет", "прив"])
async def start_handler(message: Message):
    user_id = message.from_id
    user_info = await bot.api.users.get(user_ids=user_id)
    first_name = user_info[0].first_name
    
    save_user(user_id, first_name)
    _, favorite_drink, last_mood = get_user(user_id)
    
    greeting_text = random.choice(GREETINGS).format(name=first_name)
    
    if favorite_drink or last_mood:
        greeting_text += "\n\n📋 Между прочим, я помню:"
        if favorite_drink:
            greeting_text += f"\n— Мы сошлись на том, что ты любишь {favorite_drink}. Я как раз пью его! ☕"
        if last_mood == "плохо":
            greeting_text += "\n— В прошлый раз тебе было грустно. Надеюсь, сегодня всё наладилось? Напиши, если нужно обняться."

    await send_with_typing(message, greeting_text, keyboard=get_main_keyboard())

@bot.on.message(text="🥰 сделай комплимент")
async def compliment_handler(message: Message):
    await send_with_typing(message, random.choice(COMPLIMENTS), delay=1.2)

@bot.on.message(text="💡 расскажи факт")
async def fact_handler(message: Message):
    await send_with_typing(message, random.choice(FACTS), delay=1.5)

@bot.on.message(text="☕ секретный вопрос")
async def secret_question(message: Message):
    drink_kb = (Keyboard(one_time=True)
                .add(Text("Я обожаю кофе ☕"), color=KeyboardButtonColor.PRIMARY)
                .add(Text("Только чай 🍃"), color=KeyboardButtonColor.PRIMARY)
                ).get_json()
    await send_with_typing(message, "Что спасает тебя по утрам: кофе или чай? 🧐", keyboard=drink_kb)

@bot.on.message(text=["я обожаю кофе ☕", "только чай 🍃"])
async def save_drink_handler(message: Message):
    user_id = message.from_id
    if "кофе" in message.text.lower():
        update_user_param(user_id, "favorite_drink", "кофе")
        reply = "Записал! Кофеманы правят миром. 😉"
    else:
        update_user_param(user_id, "favorite_drink", "чай")
        reply = "Чай — выбор эстетов! Запомню. ☕"
    await send_with_typing(message, reply, keyboard=get_main_keyboard(), delay=1.2)

@bot.on.message(text="✨ излить душу")
async def mood_question(message: Message):
    mood_kb = (Keyboard(one_time=True)
               .add(Text("Всё отлично!🚀"), color=KeyboardButtonColor.POSITIVE)
               .add(Text("Мне паршиво...🥺"), color=KeyboardButtonColor.NEGATIVE)
               ).get_json()
    await send_with_typing(message, "Я готов слушать. Как ты себя чувствуешь прямо сейчас?", keyboard=mood_kb)

@bot.on.message(text="всё отлично!🚀")
async def mood_good(message: Message):
    update_user_param(message.from_id, "last_mood", "отлично")
    await send_with_typing(message, "Ура! Твоя улыбка передается через экран. Так держать! 🔥", keyboard=get_main_keyboard())

@bot.on.message(text="мне паршиво...🥺")
async def mood_bad(message: Message):
    update_user_param(message.from_id, "last_mood", "плохо")
    await send_with_typing(message, "Так, иди сюда, обниму... 🤗", delay=1.0)
    await send_with_typing(message, random.choice(MOTIVATIONS), keyboard=get_main_keyboard(), delay=2.0)

@bot.on.message()
async def fallback_handler(message: Message):
    await send_with_typing(message, "Я пока только учусь свободному тексту, пользуйся кнопочками! 👇", keyboard=get_main_keyboard())

if __name__ == "__main__":
    print("Бот запущен...")
    bot.run_forever()
