
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

user_ids = set()

# === Настройки ===
BOT_TOKEN = "7652934695:AAFKpvBEbuBxHapijiACgaoLiR2fbRMCGM8"
ACCESS_PASSWORD = "нет друзей на закате"
CHAT_INVITE_LINK = "https://t.me/thelonelywolfchat"

BAD_WORDS = {
    "жопа": "💬 У нас так не принято выражаться.",
    "блять": "💬 Аккуратнее, у нас культурное сообщество.",
    "сука": "💬 Пожалуйста, без грубостей.",
    "хуй": "💬 Просим воздержаться от нецензурной лексики.",
    "ебать": "💬 Без матов, даже если фильм плохой.",
}

FAQ = {
    "что смотрим": "🎬 ну что-нибудь посмотрим,
    "где проходит просмотр": где где, дома у меня,
    "кто организатор": "👤 Организатор — Одинокий волк.",
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# <-- ВАЖНО: ВСТАВЬ СВОЙ ЧИСЛОВОЙ user_id ЗДЕСЬ:
ADMIN_ID = 123456789  # <-- замени 123456789 на свой реальный user_id

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_ids.add(user_id)
    await update.message.reply_text(
        f"Добро пожаловать в бот сообщества «Одинокий волк».\n\n"
        f"Чтобы получить доступ к нашему дискашн чат, пожалуйста, завершите фразу:\n"
        f"🌒 Мы живем в сумрачном мире\n\n"
        f"Ваш user_id: {user_id}  (Это поможет тебе узнать свой ID)"
    )

async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    message_text = update.message.text.strip().lower()

    # Если написали просто "рассылка" без слеша
    if message_text == "рассылка":
        await update.message.reply_text("❗ Для рассылки сообщений используйте команду /рассылка с текстом после неё.")
        return

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
        for bad_word in BAD_WORDS:
            if bad_word in message_text:
                await update.message.reply_text(BAD_WORDS[bad_word])
                break

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет прав на использование этой команды.")
        return

    if not context.args:
        await update.message.reply_text("❗ Напиши текст после команды /рассылка")
        return

    message = " ".join(context.args)
    count = 0
    for user_id in user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"📢 {message}")
            count += 1
        except Exception as e:
            print(f"Не удалось отправить {user_id}: {e}")

    await update.message.reply_text(f"✅ Сообщение отправлено {count} пользователям.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("рассылка", broadcast))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_password))

    print("✅ Бот запущен")
    app.run_polling()
