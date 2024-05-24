import feedparser
from telegram import Bot
from telegram.error import TelegramError
import asyncio
import os
import logging
import json

# Configuraties
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
CHANNEL_ID = '-1002013585609'  # Vervang door de chat-ID van je kanaal
RSS_FEEDS = [
    'https://www.nu.nl/rss/Algemeen',
    'https://feeds.nos.nl/nosnieuwsalgemeen',
    'https://www.ad.nl/rss.xml'
]
POSTED_ARTICLES_FILE = 'posted_articles.json'
BACKUP_FILE = 'posted_articles_backup.json'

# Logging instellen
logging.basicConfig(level=logging.DEBUG)  # Verhoog het log level naar DEBUG
logger = logging.getLogger(__name__)

EXCLUDE_KEYWORDS = ['sport', 'voetbal', 'judo', 'schaatsen', 'formule 1', 'darts']  # Voeg hier je trefwoorden toe die je wilt uitsluiten

def load_posted_articles():
    if os.path.exists(POSTED_ARTICLES_FILE):
        try:
            with open(POSTED_ARTICLES_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {POSTED_ARTICLES_FILE}, initializing empty list.")
            return []
    return []

def save_posted_articles(posted_articles):
    with open(POSTED_ARTICLES_FILE, 'w') as file:
        json.dump(posted_articles, file)
    # Maak een backup
    with open(BACKUP_FILE, 'w') as backup_file:
        json.dump(posted_articles, backup_file)
    logger.debug(f"Backup of posted articles saved to {BACKUP_FILE}")

async def fetch_news(posted_articles):
    articles = []
    for feed_url in RSS_FEEDS:
        logger.debug(f"Fetching feed: {feed_url}")
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title if 'title' in entry else ''
            description = entry.description if 'description' in entry else ''
            link = entry.link if 'link' in entry else ''
            logger.debug(f"Processing entry: {title}")
            if not any(keyword.lower() in title.lower() or keyword.lower() in description.lower() for keyword in EXCLUDE_KEYWORDS):
                if link not in posted_articles:
                    articles.append({
                        'title': title,
                        'link': link,
                        'published': entry.published if 'published' in entry else ''
                    })
                else:
                    logger.debug(f"Article already posted: {title}")
    logger.info(f"Fetched {len(articles)} new articles")
    return articles

async def send_news(bot, articles, posted_articles):
    for article in articles:
        message = f"**[{article['title']}]({article['link']})**"
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
            logger.info(f"Sent article: {article['title']}")
            posted_articles.append(article['link'])
            save_posted_articles(posted_articles)
            await asyncio.sleep(1)  # Voorkom te veel verzoeken in korte tijd
        except TelegramError as e:
            logger.error(f"Failed to send message: {e}")

async def main():
    try:
        logger.info("Starting script...")
        bot = Bot(token=API_TOKEN)
        posted_articles = load_posted_articles()
        logger.info("Fetching news...")
        articles = await fetch_news(posted_articles)
        logger.info("Sending news...")
        await send_news(bot, articles, posted_articles)
        logger.info("Script finished successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
