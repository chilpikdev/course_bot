# create_test_data.py
# Скрипт для создания тестовых данных (с поддержкой системы платежей)

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_bot_project.settings')
django.setup()

from bot.models import TelegramUser, UserState
from courses.models import Course, PaymentMethod
from payments.models import Payment, Advertisement
from decimal import Decimal

def create_test_data():
    """Создание тестовых данных для проверки работы системы"""
    
    print("🚀 Создание тестовых данных...")
    
    # 1. Создание способов оплаты
    print("\n📱 Создание способов оплаты...")
    
    payment_methods = [
        {
            'name': 'Сбербанк',
            'card_number': '2202 2023 1234 5678',
            'cardholder_name': 'Иван Петрович Сидоров',
            'bank_name': 'Сбербанк',
            'instructions': (
                'Переведите указанную сумму на карту Сбербанка:\n'
                '• Сумма должна быть точной\n'
                '• После перевода пришлите скриншот чека\n'
                '• Чек должен содержать сумму и время операции'
            ),
            'order': 1
        },
        {
            'name': 'Тинькофф',
            'card_number': '5536 9137 8765 4321',
            'cardholder_name': 'Иван Петрович Сидоров',
            'bank_name': 'Тинькофф Банк',
            'instructions': (
                'Сделайте перевод на карту Тинькофф:\n'
                '• Переводите точную сумму\n'
                '• Отправьте подтверждение об операции\n'
                '• Проверка обычно занимает до 1 часа'
            ),
            'order': 2
        },
        {
            'name': 'Qiwi Кошелек',
            'card_number': '+7 915 123-45-67',
            'cardholder_name': 'Иван Сидоров',
            'bank_name': 'Qiwi',
            'instructions': (
                'Переведите на Qiwi кошелек:\n'
                '• Номер кошелька указан выше\n'
                '• Пришлите скриншот из приложения\n'
                '• Укажите в комментарии название курса'
            ),
            'order': 3
        }
    ]
    
    for pm_data in payment_methods:
        pm, created = PaymentMethod.objects.get_or_create(
            name=pm_data['name'],
            defaults=pm_data
        )
        if created:
            print(f"✅ Создан способ оплаты: {pm.name}")
        else:
            print(f"ℹ️  Способ оплаты уже существует: {pm.name}")
    
    # 2. Создание курсов
    print("\n📚 Создание курсов...")
    
    courses_data = [
        {
            'name': 'Python для начинающих',
            'description': (
                'Полный курс по изучению языка программирования Python с нуля. '
                'Вы изучите основы синтаксиса, работу с данными, создание функций, '
                'объектно-ориентированное программирование и многое другое.\n\n'
                '📋 Что включено:\n'
                '• 50+ видеоуроков\n'
                '• Практические задания\n'
                '• Проекты для портфолио\n'
                '• Поддержка преподавателя\n'
                '• Сертификат о прохождении\n\n'
                '⏱️ Длительность: 8 недель\n'
                '🎯 Уровень: Начинающий'
            ),
            'short_description': 'Изучите Python за 8 недель с нуля до создания реальных проектов',
            'price': Decimal('2999.00'),
            'old_price': Decimal('4999.00'),
            'group_link': 'https://t.me/+python_beginners_course_group',
            'is_featured': True,
            'order': 1
        },
        {
            'name': 'Django разработка',
            'description': (
                'Углубленный курс по веб-разработке на Django. '
                'Создание полноценных веб-приложений, работа с базами данных, '
                'деплой на сервер, оптимизация и безопасность.\n\n'
                '📋 Что включено:\n'
                '• 80+ видеоуроков\n'
                '• Создание 3 реальных проектов\n'
                '• Работа с API и базами данных\n'
                '• Деплой на хостинг\n'
                '• Менторство и код-ревью\n\n'
                '⏱️ Длительность: 12 недель\n'
                '🎯 Уровень: Продвинутый'
            ),
            'short_description': 'Создавайте профессиональные веб-приложения на Django',
            'price': Decimal('4999.00'),
            'old_price': Decimal('7999.00'),
            'group_link': 'https://t.me/+django_advanced_course_group',
            'order': 2
        },
        {
            'name': 'Telegram Bot разработка',
            'description': (
                'Практический курс по созданию Telegram ботов на Python. '
                'От простых команд до сложных интерактивных ботов с базой данных, '
                'платежами и админ-панелью.\n\n'
                '📋 Что включено:\n'
                '• 30+ практических уроков\n'
                '• Создание бота с нуля\n'
                '• Интеграция с Django\n'
                '• Система платежей\n'
                '• Деплой в облако\n\n'
                '⏱️ Длительность: 6 недель\n'
                '🎯 Уровень: Средний'
            ),
            'short_description': 'Создайте своего первого Telegram бота за 6 недель',
            'price': Decimal('1999.00'),
            'group_link': 'https://t.me/+telegram_bot_course_group',
            'max_students': 50,
            'order': 3
        },
        {
            'name': 'Data Science с Python',
            'description': (
                'Комплексный курс по анализу данных и машинному обучению. '
                'Изучите pandas, numpy, matplotlib, scikit-learn и создайте '
                'собственные модели машинного обучения.\n\n'
                '📋 Что включено:\n'
                '• 60+ видеоуроков\n'
                '• Работа с реальными данными\n'
                '• Создание ML моделей\n'
                '• Визуализация данных\n'
                '• Портфолио проектов\n\n'
                '⏱️ Длительность: 10 недель\n'
                '🎯 Уровень: Продвинутый'
            ),
            'short_description': 'Станьте Data Scientist за 10 недель интенсивного обучения',
            'price': Decimal('5999.00'),
            'old_price': Decimal('8999.00'),
            'group_link': 'https://t.me/+data_science_python_group',
            'max_students': 30,
            'is_featured': True,
            'order': 4
        }
    ]
    
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            name=course_data['name'],
            defaults=course_data
        )
        if created:
            print(f"✅ Создан курс: {course.name} - {course.price} руб.")
        else:
            print(f"ℹ️  Курс уже существует: {course.name}")
    
    # 3. Создание тестовых пользователей
    print("\n👥 Создание тестовых пользователей...")
    
    users_data = [
        {
            'chat_id': 123456789,
            'username': 'test_user_1',
            'first_name': 'Алексей',
            'last_name': 'Петров',
            'phone': '+7 (915) 123-45-67'
        },
        {
            'chat_id': 987654321,
            'username': 'test_user_2',
            'first_name': 'Мария',
            'last_name': 'Иванова',
            'phone': '+7 (925) 987-65-43'
        },
        {
            'chat_id': 555666777,
            'username': 'test_user_3',
            'first_name': 'Дмитрий',
            'last_name': 'Сидоров',
            'phone': '+7 (903) 555-66-77'
        },
        {
            'chat_id': 111222333,
            'username': 'test_admin',
            'first_name': 'Администратор',
            'last_name': 'Курсов',
            'phone': '+7 (999) 111-22-33'
        }
    ]
    
    for user_data in users_data:
        user, created = TelegramUser.objects.get_or_create(
            chat_id=user_data['chat_id'],
            defaults=user_data
        )
        if created:
            print(f"✅ Создан пользователь: {user.full_name} ({user.chat_id})")
        else:
            print(f"ℹ️  Пользователь уже существует: {user.full_name}")
    
    # 4. Создание рекламных объявлений
    print("\n📢 Создание рекламных объявлений...")
    
    ads_data = [
        {
            'title': 'Новые курсы уже доступны!',
            'text': (
                '🎓 Друзья! У нас отличные новости!\n\n'
                '📚 Запускаем новые курсы по программированию:\n'
                '• Python для начинающих (-40%)\n'
                '• Django разработка (-37%)\n'
                '• Telegram Bot разработка\n'
                '• Data Science с Python (-33%)\n\n'
                '🔥 Специальные цены только до конца месяца!\n'
                '💬 Выберите курс в меню бота и начните обучение уже сегодня!\n\n'
                '🎯 Более 1000 студентов уже получили новые навыки!'
            ),
            'button_text': 'Выбрать курс',
            'button_url': 'https://t.me/your_bot_username'
        },
        {
            'title': 'Скидки на все курсы 50%!',
            'text': (
                '🔥 МЕГА РАСПРОДАЖА! 🔥\n\n'
                '💸 Скидки до 50% на ВСЕ курсы!\n'
                '⏰ Только 3 дня!\n\n'
                '📚 Успейте купить:\n'
                '• Python - от 2999₽\n'
                '• Django - от 4999₽\n'
                '• Data Science - от 5999₽\n\n'
                '🎁 БОНУС: При покупке 2 курсов - третий в подарок!\n\n'
                '👇 Не упустите шанс изменить свою карьеру!'
            ),
            'button_text': '🔥 Купить со скидкой',
            'button_url': 'https://t.me/your_bot_username'
        }
    ]
    
    for ad_data in ads_data:
        ad, created = Advertisement.objects.get_or_create(
            title=ad_data['title'],
            defaults=ad_data
        )
        if created:
            print(f"✅ Создано рекламное объявление: {ad.title}")
        else:
            print(f"ℹ️  Рекламное объявление уже существует: {ad.title}")
    
    print("\n🎉 Тестовые данные успешно созданы!")
    print("\n📋 Что теперь можно проверить:")
    print("1. Зайдите в админку: http://127.0.0.1:8000/admin/")
    print("2. Проверьте разделы:")
    print("   - Bot → Пользователи Telegram")
    print("   - Courses → Курсы и Способы оплаты")  
    print("   - Payments → Платежи и Реклама")
    print("3. Протестируйте покупку курса в боте")
    print("4. Проверьте уведомления администратору")
    
    # Статистика
    print(f"\n📊 Статистика:")
    print(f"   Пользователей: {TelegramUser.objects.count()}")
    print(f"   Курсов: {Course.objects.count()}")
    print(f"   Способов оплаты: {PaymentMethod.objects.count()}")
    print(f"   Платежей: {Payment.objects.count()}")
    print(f"   Рекламных объявлений: {Advertisement.objects.count()}")
    
    print(f"\n💡 Дополнительные команды:")
    print(f"   python test_payments.py     # Проверка системы платежей")
    print(f"   python run_simple_bot.py    # Запуск бота")
    print(f"   python manage.py check_bot_status  # Проверка статуса")

if __name__ == '__main__':
    create_test_data()