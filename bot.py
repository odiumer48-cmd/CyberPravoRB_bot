import telebot
from telebot import types
import logging
import json
import os
import random
import string
from datetime import datetime

# ========== ТВОЙ ТОКЕН ==========
TOKEN = "8589804770:AAGRwhAzYza5bDjTU_E_Vzw0zaDw3w2vAU8"

bot = telebot.TeleBot(TOKEN)
logging.basicConfig(level=logging.INFO)

# ========== ДАННЫЕ ==========
DATA_FILE = "bot_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"subscribers": [], "questions": [], "stats": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ========== КЛАВИАТУРА ==========
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "📚 Законы РБ", "⚖️ Твои права", "🚨 Что делать если...",
        "📞 Куда жаловаться", "📊 Тест по киберправу", "🔔 Подписаться на новости",
        "❓ Задать вопрос юристу", "📰 Свежие изменения", "🎮 Кибергонка",
        "🔐 Генератор паролей", "📎 Памятка PDF"
    ]
    markup.add(*buttons)
    return markup

# ========== СТАРТ ==========
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_name = message.from_user.first_name
    
    data = load_data()
    if user_id not in data["subscribers"]:
        data["subscribers"].append(user_id)
        save_data(data)
    
    bot.send_message(user_id, 
        f"👋 Привет, {user_name}!\n\n🛡️ Я бот по киберправу в Беларуси.\nРасскажу о твоих правах в интернете, законах и куда обращаться.\n\n👇 Выбери что-нибудь из меню:",
        reply_markup=main_keyboard())

# ========== ЗАКОНЫ ==========
@bot.message_handler(func=lambda message: message.text == "📚 Законы РБ")
def laws(message):
    bot.send_message(message.chat.id, 
        "📚 **Основные законы Беларуси по киберправу**\n\n"
        "🔹 **УК РБ статья 212** — Хищение имущества через компьютерную технику\n"
        "   → Штраф до 5000₽ или лишение свободы до 7 лет\n\n"
        "🔹 **УК РБ статья 178** — Оскорбление в интернете\n"
        "   → Штраф до 2000₽ или исправительные работы\n\n"
        "🔹 **Закон о персональных данных (№ 99-З)**\n"
        "   → Твои данные нельзя собирать без согласия\n\n"
        "🔹 **Декрет №8** — Майнинг и криптовалюта легальны только через ПВТ",
        parse_mode="Markdown")

# ========== ПРАВА ==========
@bot.message_handler(func=lambda message: message.text == "⚖️ Твои права")
def rights(message):
    bot.send_message(message.chat.id,
        "⚖️ **Твои права в интернете**\n\n"
        "🔐 **Право на приватность** — Никто не может требовать доступ к твоему телефону или соцсетям без решения суда.\n\n"
        "🗑️ **Право на удаление данных** — Ты можешь потребовать удалить свои персональные данные.\n\n"
        "📸 **Право на свои фото** — Школа или лагерь не могут использовать твои фото без согласия.\n\n"
        "🚫 **Право не давать согласие** — Ты можешь отказаться подписывать согласие на обработку данных.",
        parse_mode="Markdown")

# ========== ЧТО ДЕЛАТЬ ==========
@bot.message_handler(func=lambda message: message.text == "🚨 Что делать если...")
def what_to_do(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("😭 Меня оскорбили в соцсетях", callback_data="help_insult"),
        types.InlineKeyboardButton("🔓 Взломали аккаунт", callback_data="help_hack"),
        types.InlineKeyboardButton("💸 Обманули с деньгами", callback_data="help_money"),
        types.InlineKeyboardButton("📸 Мои фото выложили без спроса", callback_data="help_photo"),
        types.InlineKeyboardButton("👥 Травят в чате класса", callback_data="help_bullying"),
        types.InlineKeyboardButton("📞 Позвонили из банка", callback_data="help_bank")
    )
    bot.send_message(message.chat.id, "🚨 **Что делать в сложной ситуации?**\n\nВыбери свою проблему:", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("help_"))
def show_help(call):
    helps = {
        "insult": "😭 **Меня оскорбили в соцсетях**\n\n1. Сделай скриншоты\n2. Не отвечай агрессией\n3. Пожалуйся модераторам\n4. Если серьёзно — иди в милицию (ст. 178 УК РБ)",
        "hack": "🔓 **Взломали аккаунт**\n\n1. Попробуй восстановить пароль\n2. Напиши в поддержку\n3. Предупреди друзей\n4. Смени пароли везде\n5. Включи двухфакторку",
        "money": "💸 **Обманули с деньгами**\n\n1. Срочно заблокируй карту\n2. Сохрани переписку и чеки\n3. Иди в милицию (ст. 212 УК РБ)\n4. Чем быстрее, тем больше шансов",
        "photo": "📸 **Мои фото выложили без спроса**\n\n1. Попроси удалить\n2. Жалуйся администрации\n3. Требуй удаления по закону о персданных\n4. Если фото интимное — уголовное дело",
        "bullying": "👥 **Травят в чате**\n\n1. Сохрани скриншоты\n2. Скажи родителям или учителю\n3. Психолог может помочь\n4. Детский телефон доверия: 8-801-100-16-11",
        "bank": "📞 **Позвонили из банка**\n\n1. Положи трубку\n2. Перезвони в банк по номеру с карты\n3. Сотрудник никогда не просит код из смс"
    }
    key = call.data.split("_")[1]
    text = helps.get(key, "Ситуация сложная. Позвони родителям или на телефон доверия.")
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode="Markdown")

# ========== КУДА ЖАЛОВАТЬСЯ ==========
@bot.message_handler(func=lambda message: message.text == "📞 Куда жаловаться")
def contacts(message):
    bot.send_message(message.chat.id,
        "📞 **Куда обращаться:**\n\n"
        "🚔 **Милиция** — 102\n"
        "📞 **Детский телефон доверия** — 8-801-100-16-11\n"
        "⚖️ **Наццентр защиты персональных данных**\n"
        "📧 **Прокуратура РБ** — prokuratura.gov.by",
        parse_mode="Markdown")

# ========== ТЕСТ ==========
user_tests = {}

@bot.message_handler(func=lambda message: message.text == "📊 Тест по киберправу")
def start_test(message):
    user_id = message.chat.id
    questions = [
        {"text": "1. Можно ли оскорблять человека в интернете?", "options": ["Да, свобода слова", "Нет, это статья 178 УК РБ"], "correct": 1},
        {"text": "2. Что делать, если взломали аккаунт?", "options": ["Ничего, само пройдёт", "Сменить пароль и предупредить друзей"], "correct": 1},
        {"text": "3. Может ли школа использовать твои фото без согласия?", "options": ["Да", "Нет, нужно письменное согласие"], "correct": 1},
        {"text": "4. Что грозит за фишинг?", "options": ["Предупреждение", "До 7 лет тюрьмы"], "correct": 1},
        {"text": "5. Можно ли потребовать удалить свои данные с сайта?", "options": ["Нет", "Да, по закону"], "correct": 1},
        {"text": "6. Что делать при звонке из банка?", "options": ["Назвать код", "Положить трубку и перезвонить"], "correct": 1},
        {"text": "7. Какой пароль надёжнее?", "options": ["123456", "xK9#mP2$L5"], "correct": 1},
        {"text": "8. Что такое двухфакторка?", "options": ["Два пароля", "Дополнительный код из смс"], "correct": 1}
    ]
    user_tests[user_id] = {"step": 0, "score": 0, "questions": questions}
    send_question(user_id)

def send_question(user_id):
    test = user_tests.get(user_id)
    if not test:
        return
    step = test["step"]
    questions = test["questions"]
    if step >= len(questions):
        result = f"✅ **Твой результат: {test['score']} из {len(questions)}**\n\n"
        if test['score'] == len(questions):
            result += "🎉 Отлично! Ты хорошо знаешь свои права!"
        elif test['score'] >= 5:
            result += "👍 Неплохо! Но есть ещё что почитать."
        else:
            result += "😔 Маловато. Посмотри раздел 'Законы'."
        bot.send_message(user_id, result, parse_mode="Markdown")
        del user_tests[user_id]
        return
    
    q = questions[step]
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i, opt in enumerate(q["options"]):
        markup.add(types.InlineKeyboardButton(opt, callback_data=f"test_{step}_{i}"))
    bot.send_message(user_id, q["text"], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("test_"))
def handle_test_answer(call):
    _, step_str, answer_str = call.data.split("_")
    step = int(step_str)
    answer = int(answer_str)
    
    user_id = call.message.chat.id
    test = user_tests.get(user_id)
    if not test:
        return
    
    if answer == test["questions"][step]["correct"]:
        test["score"] += 1
        bot.answer_callback_query(call.id, "✅ Правильно!", show_alert=False)
    else:
        bot.answer_callback_query(call.id, "❌ Неправильно.", show_alert=False)
    
    test["step"] += 1
    send_question(user_id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

# ========== КИБЕРГОНКА ==========
race_users = {}

@bot.message_handler(func=lambda message: message.text == "🎮 Кибергонка")
def start_race(message):
    user_id = message.chat.id
    questions = [
        {"text": "Звонок из банка: просят код из смс. Что делать?", "options": ["Назвать код", "Положить трубку"], "correct": 1},
        {"text": "Что такое фишинг?", "options": ["Рыбалка", "Поддельные сайты"], "correct": 1},
        {"text": "Друг в Telegram просит деньги. Что делать?", "options": ["Перевести", "Позвонить другу"], "correct": 1},
        {"text": "Выиграл айфон, оплати доставку. Что делать?", "options": ["Оплатить", "Игнорировать"], "correct": 1}
    ]
    race_users[user_id] = {"step": 0, "score": 0, "questions": questions}
    send_race_question(user_id)

def send_race_question(user_id):
    race = race_users.get(user_id)
    if not race:
        return
    step = race["step"]
    questions = race["questions"]
    if step >= len(questions):
        result = f"🏁 **Гонка завершена!**\nПравильных ответов: {race['score']} из {len(questions)}\n\n"
        if race['score'] == len(questions):
            result += "🎉 Ты обогнал мошенника!"
        else:
            result += "😔 Мошенник обогнал тебя. Попробуй ещё раз!"
        bot.send_message(user_id, result, parse_mode="Markdown")
        del race_users[user_id]
        return
    
    q = questions[step]
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i, opt in enumerate(q["options"]):
        markup.add(types.InlineKeyboardButton(opt, callback_data=f"race_{step}_{i}"))
    bot.send_message(user_id, f"🏎️ **Вопрос {step+1}:**\n{q['text']}", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("race_"))
def handle_race_answer(call):
    _, step_str, answer_str = call.data.split("_")
    step = int(step_str)
    answer = int(answer_str)
    
    user_id = call.message.chat.id
    race = race_users.get(user_id)
    if not race:
        return
    
    if answer == race["questions"][step]["correct"]:
        race["score"] += 1
        bot.answer_callback_query(call.id, "✅ Правильно! Ты едешь вперёд!", show_alert=False)
    else:
        bot.answer_callback_query(call.id, "❌ Неправильно! Мошенник приближается!", show_alert=False)
    
    race["step"] += 1
    send_race_question(user_id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

# ========== ГЕНЕРАТОР ПАРОЛЕЙ ==========
@bot.message_handler(func=lambda message: message.text == "🔐 Генератор паролей")
def generate_password(message):
    length = 12
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(length))
    bot.send_message(message.chat.id, f"🔐 **Пароль:**\n`{password}`\n\n💡 Не используй один пароль везде!", parse_mode="Markdown")

# ========== ПАМЯТКА ==========
@bot.message_handler(func=lambda message: message.text == "📎 Памятка PDF")
def send_memo(message):
    memo = (
        "📄 **ПАМЯТКА ПО КИБЕРБЕЗОПАСНОСТИ**\n\n"
        "5 правил:\n"
        "1. Разные пароли\n"
        "2. Двухфакторка\n"
        "3. Проверяй ссылки\n"
        "4. Код из смс — никому\n"
        "5. Обновляй приложения\n\n"
        "Телефоны:\n"
        "102 — милиция\n"
        "8-801-100-16-11 — детский телефон доверия"
    )
    bot.send_message(message.chat.id, memo, parse_mode="Markdown")

# ========== ПОДПИСКА ==========
@bot.message_handler(func=lambda message: message.text == "🔔 Подписаться на новости")
def subscribe(message):
    data = load_data()
    user_id = message.chat.id
    if user_id not in data["subscribers"]:
        data["subscribers"].append(user_id)
        save_data(data)
        bot.send_message(user_id, "✅ Ты подписался на новости!")
    else:
        bot.send_message(user_id, "Ты уже подписан!")

# ========== ВОПРОС ЮРИСТУ ==========
@bot.message_handler(func=lambda message: message.text == "❓ Задать вопрос юристу")
def ask_lawyer(message):
    bot.send_message(message.chat.id, "❓ Напиши свой вопрос, я передам юристу:")
    bot.register_next_step_handler(message, save_question)

def save_question(message):
    data = load_data()
    if "questions" not in data:
        data["questions"] = []
    data["questions"].append({
        "user_id": message.chat.id,
        "user_name": message.from_user.first_name,
        "question": message.text,
        "date": str(datetime.now())
    })
    save_data(data)
    bot.send_message(message.chat.id, "📨 Вопрос сохранён. Юрист ответит.")

# ========== НОВОСТИ ==========
@bot.message_handler(func=lambda message: message.text == "📰 Свежие изменения")
def news(message):
    bot.send_message(message.chat.id,
        "📰 **Новости киберправа (апрель 2026)**\n\n"
        "🔹 Ужесточили наказание за кибербуллинг — до 3 лет\n"
        "🔹 Школы не могут требовать доступ к соцсетям\n"
        "🔹 За фишинг — до 7 лет тюрьмы",
        parse_mode="Markdown")

# ========== НЕИЗВЕСТНЫЕ КОМАНДЫ ==========
@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.send_message(message.chat.id, "🤔 Используй кнопки меню 👇", reply_markup=main_keyboard())

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    print("🤖 Бот запущен...")
    bot.infinity_polling()