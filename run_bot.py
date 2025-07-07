# run_bot.py
# Скрипт для запуска бота в режиме polling (для тестирования)

import os
import sys
import django
import asyncio
import logging

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_bot_project.settings')
django.setup()

from django.conf import settings

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Главная функция для запуска бота"""
    print("🤖 Запуск Telegram бота в режиме polling...")
    print(f"📱 Токен бота: {settings.TELEGRAM_BOT_TOKEN[:10]}...")
    
    if not settings.TELEGRAM_BOT_TOKEN:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не настроен в .env файле!")
        print("Получите токен от @BotFather и добавьте его в .env файл:")
        print("TELEGRAM_BOT_TOKEN=ваш_токен_здесь")
        return
    
    if settings.TELEGRAM_BOT_TOKEN == '1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789':
        print("❌ Ошибка: Используется тестовый токен!")
        print("Замените TELEGRAM_BOT_TOKEN в .env файле на реальный токен от @BotFather")
        return
    
    try:
        # Импортируем после настройки Django
        from bot.bot_handlers import setup_bot_application
        
        # Создаем приложение бота
        print("⚙️  Настройка приложения бота...")
        application = setup_bot_application()
        
        print("🔄 Инициализация бота...")
        # Инициализируем приложение
        await application.initialize()
        
        print("🧹 Очистка webhook...")
        # Удаляем webhook если он был установлен
        await application.bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook удален (используется polling)")
        
        print("🚀 Запуск бота...")
        print("✅ Бот запущен! Отправьте /start в Telegram для тестирования")
        print("❌ Для остановки нажмите Ctrl+C")
        print("-" * 50)
        
        # Запускаем polling с правильными параметрами
        await application.run_polling(
            poll_interval=1.0,  # Интервал опроса в секундах
            timeout=10,         # Таймаут запроса
            bootstrap_retries=-1,  # Бесконечные попытки переподключения
            read_timeout=30,    # Таймаут чтения
            write_timeout=30,   # Таймаут записи
            connect_timeout=30, # Таймаут подключения
            pool_timeout=30,    # Таймаут пула соединений
            stop_signals=None   # Управление сигналами
        )
        
    except KeyboardInterrupt:
        print("\n⏹️  Остановка бота...")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        print(f"❌ Ошибка: {e}")
        print("\n🔧 Возможные решения:")
        print("1. Проверьте токен бота в .env файле")
        print("2. Убедитесь что бот активен в @BotFather")
        print("3. Проверьте интернет-соединение")
        print("4. Запустите: python fix_bot_issue.py")
    finally:
        # Завершаем приложение
        try:
            if 'application' in locals():
                print("🧹 Завершение приложения...")
                await application.shutdown()
        except:
            pass
        print("👋 Бот остановлен")

if __name__ == '__main__':
    # Проверяем настройки
    if not hasattr(settings, 'TELEGRAM_BOT_TOKEN') or not settings.TELEGRAM_BOT_TOKEN:
        print("❌ Ошибка конфигурации!")
        print("Убедитесь, что:")
        print("1. Создан .env файл")
        print("2. В .env файле указан TELEGRAM_BOT_TOKEN=ваш_токен")
        print("3. Токен получен от @BotFather в Telegram")
        sys.exit(1)
    
    try:
        # Запускаем основную функцию
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        print("\n🔧 Попробуйте:")
        print("1. python fix_bot_issue.py")
        print("2. pip install --force-reinstall python-telegram-bot==20.8")
        print("3. Проверьте, что токен правильный в .env файле")
        sys.exit(1)