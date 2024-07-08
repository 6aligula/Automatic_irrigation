from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters
import os 
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Leer las variables de entorno
token_bot = os.getenv('BOT_API')

async def show_chat_id(update: Update, context):
    chat_id = update.message.chat_id
    print("Chat ID:", chat_id)
    await context.bot.send_message(chat_id=chat_id, text=f"Tu Chat ID es: {chat_id}")

def main():
    TOKEN = token_bot  # Reemplaza con el token de tu bot
    application = Application.builder().token(TOKEN).build()

    message_handler = MessageHandler(filters.TEXT, show_chat_id)
    application.add_handler(message_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
