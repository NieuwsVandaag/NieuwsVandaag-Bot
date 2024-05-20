import feedparser
from telegram import Bot
from telegram.error import TelegramError
import asyncio
import os

# Configuraties
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
CHANNEL_ID = '@NieuwsVandaag'
RSS_FEEDS = [
    'https://www.nu.nl/rss',
    'https://feeds.nos.nl/nosnieuwsalgemeen',
    'https://www.ad.nl/rss.xml'
]

async def fetch_news():
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.published
            })
    return articles

async def send_news(bot, articles):
    for article in articles:
        message = f"{article['title']}\n{article['link']}"
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=message)
            await asyncio.sleep(1)  # Voorkom te veel verzoeken in korte tijd
        except TelegramError as e:
            print(f"Failed to send message: {e}")

async def main():
    try:
        print("Starting script...")
        bot = Bot(token=API_TOKEN)
        print("Fetching news...")
        articles = await fetch_news()
        print("Sending news...")
        await send_news(bot, articles)
        print("Script finished successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
