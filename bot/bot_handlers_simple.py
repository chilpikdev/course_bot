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
    bot.add_text_handler('📚 Kurslar', handle_courses_button)
    bot.add_text_handler('ℹ️ Biz haqqımızda', handle_about_button)
    bot.add_text_handler('📞 Qollap-quwatlaw', handle_support_button)
    
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
                ["📱 Nomerdi jiberiw"]
            ], one_time_keyboard=True)
            
            ctx.reply(
                "🎓 Kurs satıp alıw ushın mo'lsherlengen botqa xosh kelipsiz!\n\n"
                "Men sizge qolaylı kurstı tańlaw hám satıp alıwǵa járdem beremen.\n"
                "Baslaw ushın telefon nomerińizdi jiberiń.",
                reply_markup=keyboard
            )
            ctx.set_state(BotStates.WAITING_CONTACT)
        else:
            # Переходим в главное меню
            show_main_menu(ctx)
            ctx.set_state(BotStates.MAIN_MENU)
    
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        ctx.reply("Qátelik júz berdi. /start buyrıǵın qaytadan teriń")

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
                "✅ Raxmet! Telefon nomerińiz saqlandı.\n\n"
                "Endi siz kurstı tańlay alasız:"
            )
            
            show_main_menu(ctx)
            ctx.set_state(BotStates.MAIN_MENU)
        else:
            keyboard = KeyboardBuilder.reply_keyboard([
                ["📱 Nomerdi jiberiw"]
            ], one_time_keyboard=True)
            
            ctx.reply(
                "❌ Ótinish, tek óz telefon nomerińizdi jiberiń.",
                reply_markup=keyboard
            )
    
    except Exception as e:
        logger.error(f"Error handling contact: {e}")
        ctx.reply("Kontaktıńızdı saqlawda qátelik júz berdi. Qaytadan urınıp kóriń.")

def handle_courses_button(bot: BotManager, update: dict):
    """Обработчик кнопки 'Курсы'"""
    ctx = MessageContext(bot, update)
    show_courses_list(ctx)

def handle_about_button(bot: BotManager, update: dict):
    """Обработчик кнопки 'О нас'"""
    ctx = MessageContext(bot, update)
    
    ctx.reply(
        "📖 <b>Biz haqqımızda</b>\n\n"
        "Biz programmalastırıw boyınsha sapalı onlayn-kurslardı usınamız.\n\n"
        "🎯 Bizim abzallıqlarımız:\n"
        "• Ámeliy tapsırmalar\n"
        "• Oqıtıwshılar tárepinen qollap-quwatlaw\n"
        "• Kurstı tamamlaǵanlıǵı haqqında sertifikatlar\n"
        "• Jabıq gruppalarǵa kiriw múmkinshiligi\n\n"
        "📞 Sorawlarıńız qaldı ma? @support adresine jazıń",
        parse_mode='HTML'
    )

def handle_support_button(bot: BotManager, update: dict):
    """Обработчик кнопки 'Поддержка'"""
    ctx = MessageContext(bot, update)
    
    ctx.reply(
        "📞 <b>Qollap-quwatlaw xızmeti</b>\n\n"
        "Eger sorawlarıńız bolsa, bizge múrájat etiń:\n\n"
        "👨‍💻 Telegram: @support\n"
        "📧 Email: support@example.com\n"
        "🕐 Jumıs waqtı: 9:00 - 21:00 (МСК)\n\n"
        "Biz sizge álbette járdem beremiz!",
        parse_mode='HTML'
    )

def handle_course_details(bot: BotManager, update: dict):
    """Обработчик показа деталей курса"""
    ctx = MessageContext(bot, update)
    
    try:
        # Извлекаем ID курса из callback_data
        course_id = int(ctx.callback_data.split('_')[1])
        course = Course.objects.get(id=course_id)
        
        # Формируем сообщение
        message = f"📚 <b>{course.name}</b>\n\n"
        message += f"{course.get_display_description()}\n\n"
        
        # Цена и скидка
        if course.discount_percentage > 0:
            message += f"💰 Bahası: <s>{course.old_price}</s> <b>{course.price} sum</b> "
            message += f"🔥 <b>(-{course.discount_percentage}%)</b>\n\n"
        else:
            message += f"💰 Bahası: <b>{course.price} sum</b>\n\n"
        
        # Информация о доступности
        if course.max_students:
            current_students = course.current_students_count
            message += f"👥 Bánt orınlar: {current_students}/{course.max_students}\n"
            
            if not course.is_available:
                message += "❌ <b>Orınlar qalmadi</b>\n\n"
            else:
                message += f"✅ Bos orınlar: {course.max_students - current_students}\n\n"
        

        
        # Кнопки
        buttons = []
        
        if course.is_available:
            buttons.append([{
                'text': f"💳 {course.price} sum-ǵa satıp alıw",
                'callback_data': f"buy_{course.id}"
            }])
        
        buttons.extend([
            [{'text': "◀️ Kurslar dizimine", 'callback_data': "back_to_courses"}],
            [{'text': "🏠 Bas menyu", 'callback_data': "back_to_menu"}]
        ])
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        
        ctx.edit_message(message, keyboard)
        ctx.set_state(BotStates.COURSE_DETAILS)
        ctx.set_data('selected_course_id', course_id)
    
    except Exception as e:
        logger.error(f"Error showing course details: {e}")
        ctx.reply("Kurs haqqında maǵlıwmat júklewde qátelik júz berdi.")

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
    
    ctx.reply("🏠 Bas menyuǵa qaytıp atırmız.")
    show_main_menu(ctx)
    ctx.set_state(BotStates.MAIN_MENU)
    
    # Очищаем данные покупки
    ctx.user_data.pop('buying_course_id', None)
    ctx.user_data.pop('payment_method_id', None)

def handle_help_command(bot: BotManager, update: dict):
    """Обработчик команды /help"""
    ctx = MessageContext(bot, update)
    
    ctx.reply(
        "🤖 <b>Járdem</b>\n\n"
        "Qoljetimli buyrıqlar:\n"
        "/start - Bot penen islewdi baslaw\n"
        "/help - Usı kórsetpeni kórsetiw\n"
        "/cancel - Bas menyuǵa qaytıw\n\n"
        "Navigaciya ushın túymelerden paydalanıń.\n\n"
        "📚 <b>Kurs qalay satıp alınadı:</b>\n"
        "1. \"📚 Kurslar\" di tańlań\n"
        "2. Qızıqtırǵan kurstı tańlań\n"
        "3. \"💳 Satıp alıw\" di basıń\n"
        "4. Tólem usılın tańlań\n"
        "5. Rekvizitler boyınsha tóleń\n"
        "6. Chek skrinshotın jiberiń\n"
        "7. Tastıyıqlanıwın kútiń\n\n"
        "Qanday da bir másele payda bolsa, qollap-quwatlaw xızmetine múrájat etiń.",
        parse_mode='HTML'
    )

def handle_photo(bot: BotManager, update: dict):
    """Обработчик фото"""
    ctx = MessageContext(bot, update)
    
    # Если пользователь ожидает загрузки чека
    if ctx.user_state == BotStates.WAITING_RECEIPT:
        handle_photo_receipt(bot, update)
    else:
        ctx.reply(
            "📸 Men siziń fotońızdı aldım.\n\n"
            "Eger siz kurs tólemi haqqında chekti jiberiwdi qáleseńiz, "
            "dáslep kurstı tańlap, \"💳 Satıp alıw\" túymesin basıń."
        )

def handle_document(bot: BotManager, update: dict):
    """Обработчик документов"""
    ctx = MessageContext(bot, update)
    
    # Если пользователь ожидает загрузки чека
    if ctx.user_state == BotStates.WAITING_RECEIPT:
        handle_document_receipt(bot, update)
    else:
        ctx.reply(
            "📄 Men siziń hújjetińizdi aldım.\n\n"
            "Eger siz kurs tólemi haqqında chekti jiberiwdi qáleseńiz, "
            "dáslep kurstı tańlap, \"💳 Satıp alıw\" túymesin basıń."
        )

# Вспомогательные функции

def show_main_menu(ctx: MessageContext):
    """Показать главное меню"""
    keyboard = KeyboardBuilder.reply_keyboard([
        ["📚 Kurslar"],
        ["ℹ️ Biz haqqımızda", "📞 Qollap-quwatlaw"]
    ])
    
    ctx.reply(
        "🏠 <b>Bas menyu</b>",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

def show_courses_list(ctx: MessageContext, edit_message: bool = False):
    """Показать список курсов"""
    try:
        # Получаем активные курсы
        courses = Course.objects.filter(is_active=True).order_by('order', 'name')
        
        if not courses:
            message = "😔 Házirshe kurslar joq.\nKeyinirek urınıp kóriń."
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
            'text': "◀️ Menyuǵa qaytıw",
            'callback_data': "back_to_menu"
        }])
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        
        message = (
            "📚 <b>Kurslar:</b>\n\n"
            "Tolıq maǵlıwmat alıw hám satıp alıw ushın kurstı tańlań:"
        )
        
        if edit_message:
            ctx.edit_message(message, keyboard)
        else:
            ctx.reply(message, keyboard, parse_mode='HTML')
        
        ctx.set_state(BotStates.COURSE_SELECTION)
    
    except Exception as e:
        logger.error(f"Error showing courses: {e}")
        ctx.reply("Kurslardı júklewde qátelik júz berdi.")

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