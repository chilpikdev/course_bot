# bot_handlers_simple.py
# Обработчики для Telegram бота без внешних библиотек (с системой платежей)

import logging
from django.utils import timezone
from bot.bot_manager import BotManager, BotStates, MessageContext, KeyboardBuilder
from bot.models import TelegramUser
from courses.models import Course
from bot.payment_handlers import (
    setup_payment_handlers, handle_photo_receipt, handle_document_receipt,
    send_payment_result_to_user
)

logger = logging.getLogger(__name__)

def setup_bot_handlers(bot: BotManager):
    """Настройка всех обработчиков бота"""
    
    # Команды
    bot.add_command_handler('start', handle_start_command)
    bot.add_command_handler('cancel', handle_cancel_command)
    bot.add_command_handler('help', handle_help_command)
    
    # Текстовые сообщения (кнопки)
    bot.add_text_handler('📚 Курсы', handle_courses_button)
    bot.add_text_handler('ℹ️ О нас', handle_about_button)
    bot.add_text_handler('📞 Поддержка', handle_support_button)
    
    # Контакт
    bot.set_contact_handler(handle_contact)
    
    # Callback обработчики
    bot.add_callback_handler('course_', handle_course_details)
    bot.add_callback_handler('back_to_courses', handle_back_to_courses)
    bot.add_callback_handler('back_to_menu', handle_back_to_menu)
    
    # Фото и документы
    bot.set_photo_handler(handle_photo)
    bot.set_document_handler(handle_document)
    
    # Настраиваем обработчики платежей
    setup_payment_handlers(bot)
    
    logger.info("All bot handlers configured successfully")

def handle_start_command(bot: BotManager, update: dict):
    """Обработчик команды /start"""
    ctx = MessageContext(bot, update)
    
    try:
        # Получаем или создаем пользователя
        telegram_user, created = TelegramUser.objects.get_or_create(
            chat_id=ctx.chat_id,
            defaults={
                'username': ctx.user.get('username'),
                'first_name': ctx.user.get('first_name', ''),
                'last_name': ctx.user.get('last_name', ''),
            }
        )
        
        if created:
            logger.info(f"New user created: {telegram_user}")
        else:
            # Обновляем информацию о пользователе
            telegram_user.username = ctx.user.get('username') or telegram_user.username
            telegram_user.first_name = ctx.user.get('first_name', '') or telegram_user.first_name
            telegram_user.last_name = ctx.user.get('last_name', '') or telegram_user.last_name
            telegram_user.save()
        
        # Обновляем активность
        telegram_user.update_activity()
        
        # Проверяем наличие номера телефона
        if not telegram_user.phone:
            # Запрашиваем контакт
            keyboard = KeyboardBuilder.reply_keyboard([
                ["📱 Поделиться номером"]
            ], one_time_keyboard=True)
            
            ctx.reply(
                "🎓 Добро пожаловать в бот для покупки курсов!\n\n"
                "Я помогу вам выбрать и купить подходящий курс.\n"
                "Для начала поделитесь своим номером телефона.",
                reply_markup=keyboard
            )
            ctx.set_state(BotStates.WAITING_CONTACT)
        else:
            # Переходим в главное меню
            show_main_menu(ctx)
            ctx.set_state(BotStates.MAIN_MENU)
    
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        ctx.reply("Произошла ошибка. Попробуйте еще раз /start")

def handle_contact(bot: BotManager, update: dict):
    """Обработчик получения контакта"""
    ctx = MessageContext(bot, update)
    
    try:
        contact = ctx.message.get('contact')
        
        if contact and contact.get('user_id') == ctx.user.get('id'):
            # Обновляем информацию о пользователе
            telegram_user = TelegramUser.objects.get(chat_id=ctx.chat_id)
            telegram_user.phone = contact.get('phone_number')
            telegram_user.first_name = contact.get('first_name') or telegram_user.first_name
            telegram_user.last_name = contact.get('last_name') or telegram_user.last_name
            telegram_user.save()
            
            logger.info(f"Contact received from user {ctx.chat_id}: {contact.get('phone_number')}")
            
            ctx.reply(
                "✅ Спасибо! Ваш номер телефона сохранен.\n\n"
                "Теперь вы можете выбрать курс:"
            )
            
            show_main_menu(ctx)
            ctx.set_state(BotStates.MAIN_MENU)
        else:
            keyboard = KeyboardBuilder.reply_keyboard([
                ["📱 Поделиться номером"]
            ], one_time_keyboard=True)
            
            ctx.reply(
                "❌ Пожалуйста, поделитесь именно своим номером телефона.",
                reply_markup=keyboard
            )
    
    except Exception as e:
        logger.error(f"Error handling contact: {e}")
        ctx.reply("Произошла ошибка при сохранении контакта. Попробуйте еще раз.")

def handle_courses_button(bot: BotManager, update: dict):
    """Обработчик кнопки 'Курсы'"""
    ctx = MessageContext(bot, update)
    show_courses_list(ctx)

def handle_about_button(bot: BotManager, update: dict):
    """Обработчик кнопки 'О нас'"""
    ctx = MessageContext(bot, update)
    
    ctx.reply(
        "📖 *О нас*\n\n"
        "Мы предлагаем качественные онлайн-курсы по программированию.\n\n"
        "🎯 Наши преимущества:\n"
        "• Практические задания\n"
        "• Поддержка преподавателей\n"
        "• Сертификаты о прохождении\n"
        "• Доступ к закрытым группам\n\n"
        "📞 Остались вопросы? Напишите @support",
        parse_mode='Markdown'
    )

def handle_support_button(bot: BotManager, update: dict):
    """Обработчик кнопки 'Поддержка'"""
    ctx = MessageContext(bot, update)
    
    ctx.reply(
        "📞 *Поддержка*\n\n"
        "Если у вас есть вопросы, обращайтесь:\n\n"
        "👨‍💻 Telegram: @support\n"
        "📧 Email: support@example.com\n"
        "🕐 Время работы: 9:00 - 21:00 (МСК)\n\n"
        "Мы обязательно вам поможем!",
        parse_mode='Markdown'
    )

def handle_course_details(bot: BotManager, update: dict):
    """Обработчик показа деталей курса"""
    ctx = MessageContext(bot, update)
    
    try:
        # Извлекаем ID курса из callback_data
        course_id = int(ctx.callback_data.split('_')[1])
        course = Course.objects.get(id=course_id)
        
        # Формируем сообщение
        message = f"📚 *{course.name}*\n\n"
        message += f"{course.get_display_description()}\n\n"
        
        # Цена и скидка
        if course.discount_percentage > 0:
            message += f"💰 Цена: ~{course.old_price}~ *{course.price} руб* "
            message += f"🔥 *(-{course.discount_percentage}%)*\n\n"
        else:
            message += f"💰 Цена: *{course.price} руб*\n\n"
        
        # Информация о доступности
        if course.max_students:
            current_students = course.current_students_count
            message += f"👥 Мест занято: {current_students}/{course.max_students}\n"
            
            if not course.is_available:
                message += "❌ *Мест больше нет*\n\n"
            else:
                message += f"✅ Доступно мест: {course.max_students - current_students}\n\n"
        

        
        # Кнопки
        buttons = []
        
        if course.is_available:
            buttons.append([{
                'text': f"💳 Купить за {course.price} руб",
                'callback_data': f"buy_{course.id}"
            }])
        
        buttons.extend([
            [{'text': "◀️ К списку курсов", 'callback_data': "back_to_courses"}],
            [{'text': "🏠 Главное меню", 'callback_data': "back_to_menu"}]
        ])
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        
        ctx.edit_message(message, keyboard)
        ctx.set_state(BotStates.COURSE_DETAILS)
        ctx.set_data('selected_course_id', course_id)
    
    except Exception as e:
        logger.error(f"Error showing course details: {e}")
        ctx.reply("Произошла ошибка при загрузке информации о курсе.")

def handle_back_to_courses(bot: BotManager, update: dict):
    """Обработчик возврата к списку курсов"""
    ctx = MessageContext(bot, update)
    show_courses_list(ctx, edit_message=True)

def handle_back_to_menu(bot: BotManager, update: dict):
    """Обработчик возврата в главное меню"""
    ctx = MessageContext(bot, update)
    
    # Удаляем inline сообщение
    try:
        bot.api.delete_message(ctx.chat_id, ctx.message['message_id'])
    except:
        pass
    
    show_main_menu(ctx)
    ctx.set_state(BotStates.MAIN_MENU)

def handle_cancel_command(bot: BotManager, update: dict):
    """Обработчик команды /cancel"""
    ctx = MessageContext(bot, update)
    
    ctx.reply("🏠 Возвращаемся в главное меню.")
    show_main_menu(ctx)
    ctx.set_state(BotStates.MAIN_MENU)
    
    # Очищаем данные покупки
    ctx.user_data.pop('buying_course_id', None)
    ctx.user_data.pop('payment_method_id', None)

def handle_help_command(bot: BotManager, update: dict):
    """Обработчик команды /help"""
    ctx = MessageContext(bot, update)
    
    ctx.reply(
        "🤖 *Помощь*\n\n"
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку\n"
        "/cancel - Вернуться в главное меню\n\n"
        "Используйте кнопки для навигации.\n\n"
        "📚 *Как купить курс:*\n"
        "1. Выберите \"📚 Курсы\"\n"
        "2. Выберите интересующий курс\n"
        "3. Нажмите \"💳 Купить\"\n"
        "4. Выберите способ оплаты\n"
        "5. Оплатите по реквизитам\n"
        "6. Пришлите скриншот чека\n"
        "7. Дождитесь подтверждения\n\n"
        "При возникновении проблем обращайтесь в поддержку.",
        parse_mode='Markdown'
    )

def handle_photo(bot: BotManager, update: dict):
    """Обработчик фото"""
    ctx = MessageContext(bot, update)
    
    # Если пользователь ожидает загрузки чека
    if ctx.user_state == BotStates.WAITING_RECEIPT:
        handle_photo_receipt(bot, update)
    else:
        ctx.reply(
            "📸 Я получил ваше фото.\n\n"
            "Если вы хотите отправить чек об оплате курса, "
            "сначала выберите курс и нажмите \"💳 Купить\"."
        )

def handle_document(bot: BotManager, update: dict):
    """Обработчик документов"""
    ctx = MessageContext(bot, update)
    
    # Если пользователь ожидает загрузки чека
    if ctx.user_state == BotStates.WAITING_RECEIPT:
        handle_document_receipt(bot, update)
    else:
        ctx.reply(
            "📄 Я получил ваш документ.\n\n"
            "Если вы хотите отправить чек об оплате курса, "
            "сначала выберите курс и нажмите \"💳 Купить\"."
        )

# Вспомогательные функции

def show_main_menu(ctx: MessageContext):
    """Показать главное меню"""
    keyboard = KeyboardBuilder.reply_keyboard([
        ["📚 Курсы"],
        ["ℹ️ О нас", "📞 Поддержка"]
    ])
    
    ctx.reply(
        "🏠 *Главное меню*\n\n"
        "Выберите действие:",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

def show_courses_list(ctx: MessageContext, edit_message: bool = False):
    """Показать список курсов"""
    try:
        # Получаем активные курсы
        courses = Course.objects.filter(is_active=True).order_by('order', 'name')
        
        if not courses:
            message = "😔 К сожалению, сейчас нет доступных курсов.\nПопробуйте позже."
            if edit_message:
                ctx.edit_message(message)
            else:
                ctx.reply(message)
            return
        
        # Создаем клавиатуру с курсами
        buttons = []
        for course in courses:
            button_text = f"📚 {course.name}"
            if course.discount_percentage > 0:
                button_text += f" (-{course.discount_percentage}%)"
            
            buttons.append([{
                'text': button_text,
                'callback_data': f"course_{course.id}"
            }])
        
        buttons.append([{
            'text': "◀️ Назад в меню",
            'callback_data': "back_to_menu"
        }])
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        
        message = (
            "📚 *Доступные курсы:*\n\n"
            "Выберите курс, чтобы узнать подробности и купить:"
        )
        
        if edit_message:
            ctx.edit_message(message, keyboard)
        else:
            ctx.reply(message, keyboard, parse_mode='Markdown')
        
        ctx.set_state(BotStates.COURSE_SELECTION)
    
    except Exception as e:
        logger.error(f"Error showing courses: {e}")
        ctx.reply("Произошла ошибка при загрузке курсов.")

# Функции для админских уведомлений (для следующих этапов)

def handle_admin_approve_payment(bot: BotManager, payment_id: int):
    """Обработать одобрение платежа администратором"""
    try:
        from payments.models import Payment
        payment = Payment.objects.get(id=payment_id)
        
        if payment.status == 'pending':
            payment.approve()
            send_payment_result_to_user(bot, payment, approved=True)
            logger.info(f"Payment {payment_id} approved by admin")
            return True
        return False
        
    except Exception as e:
        logger.error(f"Error approving payment {payment_id}: {e}")
        return False

def handle_admin_reject_payment(bot: BotManager, payment_id: int, reason: str = ""):
    """Обработать отклонение платежа администратором"""
    try:
        from payments.models import Payment
        payment = Payment.objects.get(id=payment_id)
        
        if payment.status == 'pending':
            payment.reject(comment=reason)
            send_payment_result_to_user(bot, payment, approved=False)
            logger.info(f"Payment {payment_id} rejected by admin")
            return True
        return False
        
    except Exception as e:
        logger.error(f"Error rejecting payment {payment_id}: {e}")
        return False