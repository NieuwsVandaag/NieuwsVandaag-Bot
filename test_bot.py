from telegram import Bot
from telegram.error import TelegramError
import asyncio

# Configuraties
API_TOKEN = '7116116816:AAH3HiyYWEt8GgVDFVIobBqbj9H0iFJrZpo'  # Vervang door je eigen bot-token
USER_ID = '-1002013585609'  # Vervang door je eigen gebruikers-ID

async def send_test_message():
    bot = Bot(token=API_TOKEN)
    message = "Dit is een testbericht om te controleren of de bot werkt."
    try:
        await bot.send_message(chat_id=USER_ID, text=message)
        print("Bericht succesvol verzonden.")
    except TelegramError as e:
        print(f"Fout bij het verzenden van bericht: {e}")

if __name__ == "__main__":
    asyncio.run(send_test_message())
