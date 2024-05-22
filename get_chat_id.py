import requests

API_TOKEN = '7116116816:AAH3HiyYWEt8GgVDFVIobBqbj9H0iFJrZpo'  # Vervang door je eigen bot-token

def get_updates():
    url = f'https://api.telegram.org/bot{API_TOKEN}/getUpdates'
    response = requests.get(url)
    if response.status_code == 200:
        updates = response.json()
        print(updates)
    else:
        print(f"Failed to get updates: {response.status_code}")

if __name__ == "__main__":
    get_updates()
