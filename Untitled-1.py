from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import logging

# Токен бота
TOKEN = '8037806025:AAGfOFSEDHj05FvmP_37jAMxCWsVSlsaIxQ'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)



# Создание приложения с помощью ApplicationBuilder
application = ApplicationBuilder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, я бот на Python!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Это бот, который демонстрирует основные команды. Попробуй /start.")

# Обработчик текстовых сообщений
async def handle_photo_and_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=file.file_id
        )
        if update.message.caption:
            await update.message.reply_text(update.message.caption)
    else:
        # Обработка текста, если нет фото
        user_message = update.message.text
        await update.message.reply_text(f"Ты сказал: {user_message}")

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker
    
    # Отправляем обратно стикер пользователю
    await context.bot.send_sticker(
        chat_id=update.effective_chat.id,
        sticker=sticker.file_id
    )



# Регистрация обработчиков
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_photo_and_text))
application.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

# Запуск бота
if __name__ == '__main__':
    application.run_polling()