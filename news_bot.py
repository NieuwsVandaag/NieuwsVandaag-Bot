import feedparser
from telegram import Bot
from telegram.error import TelegramError
import time
import os

# Configuraties
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
CHANNEL_ID = '@NieuwsVandaag'
RSS_FEEDS = [
    'https://www.nu.nl/rss',
    'https://feeds.nos.nl/nosnieuwsalgemeen',
    'https://www.ad.nl/rss.xml'
]

def fetch_news():
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

def send_news(bot, articles):
    for article in articles:
        message = f"{article['title']}\n{article['link']}"
        try:
            bot.send_message(chat_id=CHANNEL_ID, text=message)
            time.sleep(1)  # Voorkom te veel verzoeken in korte tijd
        except TelegramError as e:
            print(f"Failed to send message: {e}")

def main():
    bot = Bot(token=API_TOKEN)
    while True:
        articles = fetch_news()
        send_news(bot, articles)
        # Wacht 24 uur voor de volgende update
        time.sleep(86400)

if __name__ == "__main__":
    main()
import feedparser
from telegram import Bot, TelegramError
import time
import os

# Configuraties
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
CHANNEL_ID = '@NieuwsVandaag'
RSS_FEEDS = [
    'https://www.nu.nl/rss',
    'https://feeds.nos.nl/nosnieuwsalgemeen',
    'https://www.ad.nl/rss.xml'
]

def fetch_news():
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

def send_news(bot, articles):
    for article in articles:
        message = f"{article['title']}\n{article['link']}"
        try:
            bot.send_message(chat_id=CHANNEL_ID, text=message)
            time.sleep(1)  # Voorkom te veel verzoeken in korte tijd
        except TelegramError as e:
            print(f"Failed to send message: {e}")

def main():
    try:
        bot = Bot(token=API_TOKEN)
        articles = fetch_news()
        send_news(bot, articles)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
