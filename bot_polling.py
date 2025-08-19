import requests
import time
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_bot_project.settings') 
django.setup()


from bot.bot_manager import BotManager
from bot.bot_handlers_simple import setup_bot_handlers

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'
OFFSET = None

_bot_instance = None

def get_bot_instance():
    """Получить экземпляр бота (singleton)"""
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = BotManager(BOT_TOKEN)
        setup_bot_handlers(_bot_instance)
    return _bot_instance

bot = get_bot_instance()   

while True:
    try:
        params = {'timeout': 30}
        if OFFSET:
            params['offset'] = OFFSET
    
        response = requests.get(f'{API_URL}/getUpdates', params=params, timeout=35)
        result = response.json()
    
        if result.get("ok"):
            updates = result.get("result", [])      
            for update in updates:
                bot.process_update(update)
                OFFSET = update['update_id'] + 1        
        else:
            print("Error:", result)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

