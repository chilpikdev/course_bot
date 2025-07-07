# test_payments.py
# Тест системы платежей для Telegram бота

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_bot_project.settings')
django.setup()

from django.conf import settings
from django.core.files.base import ContentFile

def test_imports():
    """Тест импортов системы платежей"""
    print("📦 Тестирование импортов системы платежей...")
    
    try:
        from bot.payment_handlers import (
            setup_payment_handlers, handle_photo_receipt, 
            handle_document_receipt, create_payment_record,
            send_admin_notification, send_payment_result_to_user
        )
        print("   ✅ payment_handlers")
        
        from payments.models import Payment, PaymentNotification
        print("   ✅ Payment models")
        
        from courses.models import PaymentMethod
        print("   ✅ PaymentMethod model")
        
        from bot.bot_manager import BotManager
        print("   ✅ BotManager")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Ошибка импорта: {e}")
        return False

def test_payment_methods():
    """Тест способов оплаты"""
    print("\n💳 Тестирование способов оплаты...")
    
    try:
        from courses.models import PaymentMethod
        
        methods = PaymentMethod.objects.filter(is_active=True)
        print(f"   ✅ Найдено {methods.count()} активных способов оплаты")
        
        for method in methods:
            print(f"      - {method.name}: {method.card_number}")
        
        if methods.count() == 0:
            print("   ⚠️  Нет способов оплаты. Запустите: python create_test_data.py")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

def test_payment_creation():
    """Тест создания платежа"""
    print("\n💰 Тестирование создания платежей...")
    
    try:
        from bot.models import TelegramUser
        from courses.models import Course, PaymentMethod
        from bot.payment_handlers import create_payment_record
        
        # Берем тестовые данные
        user = TelegramUser.objects.first()
        course = Course.objects.filter(is_active=True).first()
        method = PaymentMethod.objects.filter(is_active=True).first()
        
        if not all([user, course, method]):
            print("   ❌ Нет тестовых данных. Запустите: python create_test_data.py")
            return False
        
        # Создаем тестовый файл чека
        test_image_content = b"fake image content for testing"
        
        # Тестируем создание платежа
        payment = create_payment_record(
            user=user,
            course=course,
            payment_method=method,
            file_content=test_image_content,
            file_name="test_receipt.jpg",
            user_comment="Тестовый платеж"
        )
        
        if payment:
            print(f"   ✅ Платеж создан: #{payment.id}")
            print(f"      Пользователь: {payment.user.full_name}")
            print(f"      Курс: {payment.course.name}")
            print(f"      Сумма: {payment.amount} руб")
            print(f"      Статус: {payment.get_status_display()}")
            
            # Удаляем тестовый платеж
            payment.delete()
            print("   ✅ Тестовый платеж удален")
            
            return True
        else:
            print("   ❌ Не удалось создать платеж")
            return False
        
    except Exception as e:
        print(f"   ❌ Ошибка создания платежа: {e}")
        return False

def test_bot_handlers():
    """Тест обработчиков бота"""
    print("\n🤖 Тестирование обработчиков бота...")
    
    try:
        from bot.bot_manager import BotManager
        from bot.bot_handlers_simple import setup_bot_handlers
        from bot.payment_handlers import setup_payment_handlers
        
        # Создаем бота
        bot = BotManager(settings.TELEGRAM_BOT_TOKEN)
        
        # Настраиваем обработчики
        setup_bot_handlers(bot)
        
        # Проверяем наличие обработчиков платежей
        payment_handlers = [
            'buy_', 'payment_method_', 'confirm_payment_', 'cancel_payment'
        ]
        
        for handler in payment_handlers:
            if handler in bot.handlers['callback']:
                print(f"   ✅ Обработчик {handler} зарегистрирован")
            else:
                print(f"   ❌ Обработчик {handler} не найден")
                return False
        
        # Проверяем обработчики фото и документов
        if bot.handlers['photo'] and bot.handlers['document']:
            print("   ✅ Обработчики файлов настроены")
        else:
            print("   ❌ Обработчики файлов не настроены")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка обработчиков: {e}")
        return False

def test_admin_settings():
    """Тест настроек админа"""
    print("\n👨‍💼 Тестирование настроек администратора...")
    
    # Проверяем токен бота
    if not settings.TELEGRAM_BOT_TOKEN:
        print("   ❌ TELEGRAM_BOT_TOKEN не настроен")
        return False
    
    if settings.TELEGRAM_BOT_TOKEN.startswith('1234567890'):
        print("   ❌ Используется тестовый токен")
        return False
    
    print("   ✅ Токен бота настроен")
    
    # Проверяем админский chat_id
    admin_chat_id = getattr(settings, 'TELEGRAM_ADMIN_CHAT_ID', None)
    if admin_chat_id:
        print(f"   ✅ Admin chat ID настроен: {admin_chat_id}")
    else:
        print("   ⚠️  TELEGRAM_ADMIN_CHAT_ID не настроен (уведомления админу не будут работать)")
        print("      Добавьте в .env: TELEGRAM_ADMIN_CHAT_ID=ваш_chat_id")
        print("      Узнать chat_id можно у бота @userinfobot")
    
    # Проверяем медиа директории
    media_root = settings.MEDIA_ROOT
    if os.path.exists(media_root):
        print(f"   ✅ Медиа директория существует: {media_root}")
    else:
        print(f"   ⚠️  Медиа директория не существует: {media_root}")
    
    return True

def test_database_structure():
    """Тест структуры базы данных"""
    print("\n🗄️  Тестирование структуры базы данных...")
    
    try:
        from payments.models import Payment, PaymentNotification
        from courses.models import PaymentMethod
        
        # Проверяем таблицы
        tables_to_check = [
            (Payment, "payments_payment"),
            (PaymentNotification, "payments_paymentnotification"), 
            (PaymentMethod, "courses_paymentmethod")
        ]
        
        for model, table_name in tables_to_check:
            try:
                count = model.objects.count()
                print(f"   ✅ Таблица {table_name}: {count} записей")
            except Exception as e:
                print(f"   ❌ Ошибка таблицы {table_name}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка структуры БД: {e}")
        return False

def test_telegram_connection():
    """Тест подключения к Telegram"""
    print("\n🔗 Тестирование подключения к Telegram...")
    
    try:
        from bot.telegram_api import TelegramAPI
        
        api = TelegramAPI(settings.TELEGRAM_BOT_TOKEN)
        bot_info = api.get_me()
        
        print(f"   ✅ Бот подключен: @{bot_info.get('username')}")
        print(f"      Имя: {bot_info.get('first_name')}")
        print(f"      ID: {bot_info.get('id')}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка подключения: {e}")
        return False

def create_test_payment_data():
    """Создать тестовые данные для платежей"""
    print("\n📊 Создание дополнительных тестовых данных...")
    
    try:
        from courses.models import PaymentMethod
        
        # Проверяем, есть ли способы оплаты
        if PaymentMethod.objects.count() == 0:
            print("   📱 Создание тестовых способов оплаты...")
            
            methods_data = [
                {
                    'name': 'Сбербанк',
                    'card_number': '2202 2023 1234 5678',
                    'cardholder_name': 'IVAN PETROV',
                    'bank_name': 'Сбербанк',
                    'instructions': 'Переведите точную сумму на карту и пришлите скриншот.',
                    'order': 1
                },
                {
                    'name': 'Тинькофф',
                    'card_number': '5536 9137 8765 4321', 
                    'cardholder_name': 'IVAN PETROV',
                    'bank_name': 'Тинькофф Банк',
                    'instructions': 'Сделайте перевод и отправьте подтверждение.',
                    'order': 2
                }
            ]
            
            for method_data in methods_data:
                method, created = PaymentMethod.objects.get_or_create(
                    name=method_data['name'],
                    defaults=method_data
                )
                if created:
                    print(f"      ✅ Создан способ оплаты: {method.name}")
        
        print("   ✅ Тестовые данные готовы")
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка создания данных: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ ПЛАТЕЖЕЙ")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database_structure,
        test_telegram_connection,
        create_test_payment_data,
        test_payment_methods,
        test_payment_creation,
        test_bot_handlers,
        test_admin_settings
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   ❌ Критическая ошибка в тесте: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Результаты тестирования:")
    print(f"   ✅ Пройдено: {passed}")
    print(f"   ❌ Провалено: {failed}")
    
    if failed == 0:
        print("\n🎉 Все тесты пройдены! Система платежей готова!")
        print("\n🚀 Готово к запуску:")
        print("python run_simple_bot.py")
        print("\n💡 Не забудьте:")
        print("1. Настроить TELEGRAM_ADMIN_CHAT_ID в .env")
        print("2. Протестировать покупку курса в боте")
        print("3. Проверить уведомления в админке")
        return True
    else:
        print(f"\n❌ Есть {failed} проблем(ы). Исправьте их перед запуском.")
        print("\n🔧 Возможные решения:")
        print("1. Выполните: python manage.py migrate")
        print("2. Создайте данные: python create_test_data.py")
        print("3. Проверьте токен в .env файле")
        print("4. Настройте TELEGRAM_ADMIN_CHAT_ID")
        return False

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Тест прерван")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)