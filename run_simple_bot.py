# run_simple_bot.py
# Простой запуск Telegram бота без внешних библиотек

import os
import sys
import django
import logging

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_bot_project.settings')
django.setup()

from django.conf import settings
from bot.bot_manager import BotManager
from bot.bot_handlers_simple import setup_bot_handlers

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Главная функция запуска бота"""
    print("🤖 Запуск простого Telegram бота...")
    print(f"📱 Токен бота: {settings.TELEGRAM_BOT_TOKEN[:10]}...")
    
    # Проверка токена
    if not settings.TELEGRAM_BOT_TOKEN:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не настроен в .env файле!")
        print("Получите токен от @BotFather и добавьте его в .env файл:")
        print("TELEGRAM_BOT_TOKEN=ваш_токен_здесь")
        return False
    
    if settings.TELEGRAM_BOT_TOKEN.startswith('1234567890'):
        print("❌ Ошибка: Используется тестовый токен!")
        print("Замените TELEGRAM_BOT_TOKEN в .env файле на реальный токен от @BotFather")
        return False
    
    try:
        # Создаем бота
        print("⚙️  Создание бота...")
        bot = BotManager(settings.TELEGRAM_BOT_TOKEN)
        
        # Настраиваем обработчики
        print("🔧 Настройка обработчиков...")
        setup_bot_handlers(bot)
        
        # Проверяем подключение
        print("🔍 Проверка подключения к Telegram...")
        bot_info = bot.api.get_me()
        print(f"✅ Бот подключен: @{bot_info.get('username')} ({bot_info.get('first_name')})")
        
        # Запускаем polling
        print("🚀 Запуск polling...")
        print("✅ Бот запущен! Отправьте /start в Telegram для тестирования")
        print("❌ Для остановки нажмите Ctrl+C")
        print("-" * 50)
        
        bot.start_polling(interval=1.0)
        
    except KeyboardInterrupt:
        print("\n⏹️  Остановка бота...")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        print(f"❌ Ошибка: {e}")
        print("\n🔧 Возможные решения:")
        print("1. Проверьте токен бота в .env файле")
        print("2. Убедитесь что бот активен в @BotFather")
        print("3. Проверьте интернет-соединение")
        print("4. Проверьте настройки Django")
        return False
    finally:
        print("👋 Бот остановлен")
    
    return True

if __name__ == '__main__':
    # Проверяем настройки Django
    try:
        from bot.models import TelegramUser
        from courses.models import Course
        print("✅ Django модели доступны")
    except Exception as e:
        print(f"❌ Ошибка Django: {e}")
        print("Выполните: python manage.py migrate")
        sys.exit(1)
    
    # Проверяем настройки
    if not hasattr(settings, 'TELEGRAM_BOT_TOKEN') or not settings.TELEGRAM_BOT_TOKEN:
        print("❌ Ошибка конфигурации!")
        print("Убедитесь, что:")
        print("1. Создан .env файл")
        print("2. В .env файле указан TELEGRAM_BOT_TOKEN=ваш_токен")
        print("3. Токен получен от @BotFather в Telegram")
        sys.exit(1)
    
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)