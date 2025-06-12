import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# === Настройки ===
BOT_TOKEN = "7652934695:AAFKpvBEbuBxHapijiACgaoLiR2fbRMCGM8"  # <-- вставь сюда токен бота
ACCESS_PASSWORD = "нет друзей на закате"  # пароль для вступления
CHAT_INVITE_LINK = "https://t.me/thelonelywolfchat"  # <-- вставь ссылку-приглашение в чат

# Нецензурные слова и предупреждения
BAD_WORDS = {
    "жопа": "💬 У нас так не принято выражаться.",
    "блять": "💬 Аккуратнее, у нас культурное сообщество.",
    "сука": "💬 Пожалуйста, без грубостей.",
    "хуй": "💬 Просим воздержаться от нецензурной лексики.",
    "ебать": "💬 Без матов, даже если фильм плохой.",
    # добавь свои слова и ответы
}

# Популярные автоответы (можно расширить)
FAQ = {
    "что смотрим": "🎬 Сегодня смотрим «Олдбой» (2003). Начало в 20:00.",
    "где проходит просмотр": "📍 Онлайн в нашем закрытом чате.",
    "кто организатор": "👤 Организатор — Одинокий волк.",
    # добавь другие варианты
}

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# === Обработка команды /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌒 Мы живем в сумрачном мире.\n\n"
        "Добро пожаловать в бот сообщества «Одинокий волк». "
        "Чтобы получить доступ к нашему закрытому кинозалу, пожалуйста, введите пароль:"
    )

# === Проверка пароля ===
async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    message_text = update.message.text.strip().lower()

    if message_text == ACCESS_PASSWORD:
        keyboard = [[InlineKeyboardButton("👥 Вступить в чат", url=CHAT_INVITE_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "✅ Пароль принят.\n\nНажми на кнопку, чтобы вступить в наш уютный кинозал:",
            reply_markup=reply_markup
        )
    elif message_text in FAQ:
        await update.message.reply_text(FAQ[message_text])
    else:
        # Проверка на мат
        for bad_word in BAD_WORDS:
            if bad_word in message_text:
                await update.message.reply_text(BAD_WORDS[bad_word])
                break

# === Старт приложения ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_password))

    print("✅ Бот запущен")
    app.run_polling()
