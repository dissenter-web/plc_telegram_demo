from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from app.config import BOT_TOKEN, DATA_FILE
from app.storage import Storage


storage = Storage(DATA_FILE)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat:
        storage.set_active_chat(chat.id)

    if update.message:
        await update.message.reply_text("Подключено")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()


if __name__ == "__main__":
    main()