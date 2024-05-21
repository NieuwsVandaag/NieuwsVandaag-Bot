import feedparser
from telegram import Bot
from telegram.error import TelegramError
import asyncio
import os
import logging

# Configuraties
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
CHANNEL_ID = '-1002013585609'  # Vervang door de chat-ID van je kanaal
RSS_FEEDS = [
    'https://www.nu.nl/rss',
    'https://feeds.nos.nl/nosnieuwsalgemeen',
    'https://www.ad.nl/rss.xml'
]

# Logging instellen
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KEYWORDS = ['technologie', 'politiek', 'sport']  # Voeg hier je trefwoorden toe

async def fetch_news():
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            if any(keyword.lower() in entry.title.lower() or keyword.lower() in entry.description.lower() for keyword in KEYWORDS):
                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published
                })
    logger.info(f"Fetched {len(articles)} articles")
    return articles

async def send_news(bot, articles):
    for article in articles:
        message = f"**{article['title']}**\n{article['link']}\n_Gepubliceerd op: {article['published']}_"
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
            logger.info(f"Sent article: {article['title']}")
            await asyncio.sleep(1)  # Voorkom te veel verzoeken in korte tijd
        except TelegramError as e:
            logger.error(f"Failed to send message: {e}")

async def main():
    try:
        logger.info("Starting script...")
        bot = Bot(token=API_TOKEN)
        logger.info("Fetching news...")
        articles = await fetch_news()
        logger.info("Sending news...")
        await send_news(bot, articles)
        logger.info("Script finished successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
