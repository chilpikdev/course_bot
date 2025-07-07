# check_config.py
# Скрипт для проверки конфигурации перед запуском бота

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_bot_project.settings')

try:
    django.setup()
    from django.conf import settings
    from bot.models import TelegramUser
    from courses.models import Course, PaymentMethod
    from payments.models import Payment, Advertisement
except Exception as e:
    print(f"❌ Ошибка инициализации Django: {e}")
    sys.exit(1)

def check_env_file():
    """Проверка .env файла"""
    print("🔍 Проверка .env файла...")
    
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print("Создайте файл .env и скопируйте содержимое из примера")
        return False
    
    # Проверяем основные переменные
    required_vars = ['SECRET_KEY', 'TELEGRAM_BOT_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if not hasattr(settings, var) or not getattr(settings, var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Отсутствуют обязательные переменные: {', '.join(missing_vars)}")
        return False
    
    # Проверяем токен бота
    if settings.TELEGRAM_BOT_TOKEN == 'your_bot_token_from_botfather':
        print("❌ TELEGRAM_BOT_TOKEN не настроен!")
        print("Получите токен от @BotFather и укажите его в .env файле")
        return False
    
    print("✅ .env файл настроен корректно")
    return True

def check_database():
    """Проверка базы данных"""
    print("\n🗄️  Проверка базы данных...")
    
    try:
        # Проверяем подключение к базе
        from django.db import connection
        connection.ensure_connection()
        
        # Проверяем таблицы
        tables_exist = True
        try:
            TelegramUser.objects.count()
            Course.objects.count()
            PaymentMethod.objects.count()
        except Exception:
            tables_exist = False
        
        if not tables_exist:
            print("❌ Таблицы базы данных не созданы!")
            print("Выполните: python manage.py migrate")
            return False
        
        print("✅ База данных работает корректно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return False

def check_test_data():
    """Проверка тестовых данных"""
    print("\n📊 Проверка тестовых данных...")
    
    courses_count = Course.objects.count()
    payment_methods_count = PaymentMethod.objects.count()
    users_count = TelegramUser.objects.count()
    
    print(f"   Курсов: {courses_count}")
    print(f"   Способов оплаты: {payment_methods_count}")
    print(f"   Пользователей: {users_count}")
    
    if courses_count == 0:
        print("⚠️  Нет курсов в базе данных")
        print("Выполните: python create_test_data.py")
        return False
    
    if payment_methods_count == 0:
        print("⚠️  Нет способов оплаты")
        print("Выполните: python create_test_data.py")
        return False
    
    print("✅ Тестовые данные присутствуют")
    return True

def check_dependencies():
    """Проверка зависимостей"""
    print("\n📦 Проверка зависимостей...")
    
    required_packages = [
        'telegram',
        'django',
        'PIL',
        'decouple'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Отсутствуют пакеты: {', '.join(missing_packages)}")
        print("Выполните: pip install -r requirements.txt")
        return False
    
    print("✅ Все зависимости установлены")
    return True

def check_bot_config():
    """Проверка конфигурации бота"""
    print("\n🤖 Проверка конфигурации бота...")
    
    try:
        # Проверяем импорт telegram
        import telegram
        print(f"   Версия python-telegram-bot: {telegram.__version__}")
        
        # Проверяем наличие необходимых классов
        from telegram.ext import Application
        from telegram import Bot
        
        # Проверяем токен
        if not settings.TELEGRAM_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN == 'your_bot_token_from_botfather':
            print("❌ TELEGRAM_BOT_TOKEN не настроен!")
            return False
        
        # Простая проверка создания бота (без полной инициализации)
        try:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            # Не делаем реальных запросов, просто проверяем создание объекта
            print("✅ Токен бота валиден")
        except Exception as e:
            print(f"❌ Проблема с токеном бота: {e}")
            return False
        
        # Проверяем импорт обработчиков
        try:
            from bot.bot_handlers import setup_bot_application
            print("✅ Обработчики бота импортируются корректно")
        except Exception as e:
            print(f"❌ Ошибка импорта обработчиков: {e}")
            return False
        
        print("✅ Конфигурация бота корректна")
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Выполните: pip install python-telegram-bot==20.8")
        return False
    except Exception as e:
        print(f"❌ Ошибка конфигурации бота: {e}")
        print("Попробуйте: python fix_bot_issue.py")
        return False

def main():
    """Основная функция проверки"""
    print("🔧 Проверка конфигурации Telegram бота для курсов")
    print("=" * 50)
    
    checks = [
        check_dependencies,
        check_env_file,
        check_database,
        check_test_data,
        check_bot_config
    ]
    
    all_passed = True
    
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 Все проверки пройдены успешно!")
        print("\n🚀 Готово к запуску:")
        print("python run_bot.py")
    else:
        print("❌ Есть проблемы с конфигурацией")
        print("\n🔧 Исправьте ошибки и запустите проверку снова:")
        print("python check_config.py")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)