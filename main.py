
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ChatMemberHandler,
    ContextTypes, filters
)

# === НАСТРОЙКИ ===
TOKEN = '7652934695:AAFKpvBEbuBxHapijiACgaoLiR2fbRMCGM8'
CHAT_INVITE_LINK = 'https://t.me/thelonelywolfchat'
ACCESS_PASSWORD = 'нет друзей на закате'

# Триггеры нецензурной лексики (добавляй свои)
BAD_WORDS = {
    "жопа": "🛑 У нас так не выражаются.",
    "блять": "🤐 Аккуратнее, пожалуйста.",
    "нахуй": "⚠️ Без агрессии, давай уважительно.",
    "сука": "🚫 Воздержись от подобных слов.",
    "ебать": "👀 Слишком грубо для киноклуба.",
}

# === Проверка пароля ===
async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.strip().lower()
    
    # Если это пароль — даём кнопку
    if message_text == ACCESS_PASSWORD:
        keyboard = [[InlineKeyboardButton("👥 Вступить в чат", url=CHAT_INVITE_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "✅ Пароль принят.\n\nНажми на кнопку, чтобы вступить в наш уютный кинозал:",
            reply_markup=reply_markup
        )
    # Если это плохое слово
    elif message_text in BAD_WORDS:
        await update.message.reply_text(BAD_WORDS[message_text])
    else:
        await update.message.reply_text("❌ Неверный пароль. Попробуй ещё раз.")

# === Приветствие новых участников в чате ===
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.chat_member
    if member.new_chat_member.status == "member":
        await context.bot.send_message(
            chat_id=update.chat_member.chat.id,
            text=(
                "👋 Добро пожаловать в чат *Одинокий волк*!\n\n"
                "📜 *Наши правила:*\n"
                "1️⃣ Уважай других участников\n"
                "2️⃣ Без мата и оскорблений\n"
                "3️⃣ Не спамь, не флууди\n"
                "4️⃣ Делясь мнением — будь душевным\n"
                "5️⃣ За нарушения — предупреждение или удаление\n\n"
                "🎬 Приятного просмотра и общения!"
            ),
            parse_mode='Markdown'
        )

# === Запуск бота ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Проверка текста (пароль + маты)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_password))

    # Обработка вступления в чат
    app.add_handler(ChatMemberHandler(new_member, ChatMemberHandler.CHAT_MEMBER))

    print("🤖 Бот запущен и ждёт пользователей...")
    app.run_polling()

if __name__ == "__main__":
    main()
	
