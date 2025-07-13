# payment_handlers.py
# Обработчики системы платежей для Telegram бота

import os
import logging
from datetime import datetime
from django.core.files.base import ContentFile
from django.conf import settings
from bot.bot_manager import BotManager, BotStates, MessageContext, KeyboardBuilder
from bot.models import TelegramUser
from courses.models import Course, PaymentMethod
from payments.models import Payment, PaymentNotification
from django.utils import timezone


logger = logging.getLogger(__name__)

def setup_payment_handlers(bot: BotManager):
    """Настройка обработчиков платежей"""
    
    # Callback обработчики для платежей
    bot.add_callback_handler('buy_', handle_buy_course)
    bot.add_callback_handler('payment_method_', handle_payment_method_selection)
    bot.add_callback_handler('confirm_payment_', handle_confirm_payment)
    bot.add_callback_handler('cancel_payment', handle_cancel_payment)
    
    logger.info("Payment handlers configured successfully")

def handle_buy_course(bot: BotManager, update: dict):
    """Обработчик начала покупки курса"""
    ctx = MessageContext(bot, update)
    
    try:
        # Извлекаем ID курса
        course_id = int(ctx.callback_data.split('_')[1])
        course = Course.objects.get(id=course_id)
        
        # Проверяем доступность курса
        if not course.is_available:
            ctx.edit_message(
                "❌ Ókinishke oray, bul kurs endi qoljetimli emes.",
                KeyboardBuilder.inline_keyboard([[
                    {'text': "◀️ Kurslar dizimine", 'callback_data': "back_to_courses"}
                ]])
            )
            return
        
        # Проверяем, не покупал ли пользователь этот курс ранее
        telegram_user = TelegramUser.objects.get(chat_id=ctx.chat_id)
        existing_payment = Payment.objects.filter(
            user=telegram_user, 
            course=course,
            status__in=['approved', 'pending']
        ).first()
        
        if existing_payment:
            if existing_payment.status == 'approved':
                ctx.edit_message(
                    f"✅ Siz \"{course.name}\" kursın satıp alıp bolǵansız.\n\n"
                    f"Gruppaǵa silteme: {course.group_link}",
                    KeyboardBuilder.inline_keyboard([[
                        {'text': "◀️ Kurslar dizimine", 'callback_data': "back_to_courses"}
                    ]])
                )
            else:
                ctx.edit_message(
                    f"⏳ Sizde \"{course.name}\" kursın satıp alıw ushın arza bar.\n"
                    f"Statusı: {existing_payment.get_status_display()}\n\n"
                    f"Administratordıń tekseriwin kútiń.",
                    KeyboardBuilder.inline_keyboard([[
                        {'text': "◀️ Kurslar dizimine", 'callback_data': "back_to_courses"}
                    ]])
                )
            return
        
        # Получаем доступные способы оплаты
        payment_methods = PaymentMethod.objects.filter(is_active=True).order_by('order')
        
        if not payment_methods:
            ctx.edit_message(
                "❌ Ókinishke oray, házir tólemniń qoljetimli usılları joq.\n"
                "Qollap-quwatlaw xızmetine múrájat etiń.",
                KeyboardBuilder.inline_keyboard([[
                    {'text': "◀️ Artqa", 'callback_data': f"course_{course_id}"}
                ]])
            )
            return
        
        if payment_methods.count() == 1:
            fake_update = update.copy()
            fake_update['callback_query'] = fake_update.get('callback_query', {})
            fake_update['callback_query']['data'] = f"payment_method_{course_id}_{payment_methods.first().id}"
            handle_payment_method_selection(bot, fake_update)
            return

        # Формируем сообщение с выбором способа оплаты
        message = f"💳 <b>Kurs satıp alıw: {course.name}</b>\n\n"
        message += f"💰 Bahası: <b>{course.price} sum</b>\n\n"
        message += "Tólem usılın tańlań:"
        
        # Кнопки способов оплаты
        buttons = []
        for method in payment_methods:
            buttons.append([{
                'text': f"💳 {method.name}",
                'callback_data': f"payment_method_{course_id}_{method.id}"
            }])
        
        buttons.append([{
            'text': "❌ Biykar etiw",
            'callback_data': f"course_{course_id}"
        }])
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        
        ctx.edit_message(message, keyboard)
        ctx.set_state(BotStates.PAYMENT_METHOD)
        ctx.set_data('buying_course_id', course_id)
        
    except Exception as e:
        logger.error(f"Error in buy course: {e}")
        ctx.reply("Satıp alıwdı rásmiylestiriwde qátelik júz berdi.")

def handle_payment_method_selection(bot: BotManager, update: dict):
    """Обработчик выбора способа оплаты"""
    ctx = MessageContext(bot, update)
    
    try:
        # Извлекаем данные из callback
        parts = ctx.callback_data.split('_')
        course_id = int(parts[2])
        method_id = int(parts[3])
        
        course = Course.objects.get(id=course_id)
        payment_method = PaymentMethod.objects.get(id=method_id)
        
        # Формируем сообщение с реквизитами
        message = f"💳 <b>Kurs tólemi: {course.name}</b>\n\n"
        message += f"💰 Tólem ushın summa: <b>{course.price} sum</b>\n\n"
        message += f"📋 <b>Tólem ushın rekvizitler:</b>\n\n"
        message += payment_method.get_payment_info()
        message += f"\n\n⚠️ <b>Áhmiyetli:</b>\n"
        message += f"• Anıq <b>{course.price} sum</b> ótkeriwiz kerek\n"
        message += f"• Tólemnen keyin chektiń skrinshotın jiberiń\n"
        message += f"• Administrator tólemdi tekseredi hám gruppa siltemesin jiberedi\n\n"
        message += f"📸 Chektiń skrinshotın yamasa PDF hújjetin jiberiń:"
        
        buttons = [
            [{'text': "❌ Satıp alıwdı biykarlaw", 'callback_data': "cancel_payment"}],
            [{'text': "◀️ Artqa", 'callback_data': f"course_{course_id}"}]
        ]
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        
        ctx.edit_message(message, keyboard)
        ctx.set_state(BotStates.WAITING_RECEIPT)
        ctx.set_data('buying_course_id', course_id)
        ctx.set_data('payment_method_id', method_id)
        
    except Exception as e:
        logger.error(f"Error in payment method selection: {e}")
        ctx.reply("Tólem usılın tańlawda qátelik júz berdi.")

def handle_photo_receipt(bot: BotManager, update: dict):
    """Обработчик получения фото чека"""
    ctx = MessageContext(bot, update)
    
    if ctx.user_state != BotStates.WAITING_RECEIPT:
        return
    
    try:
        # Получаем данные о покупке
        course_id = ctx.user_data.get('buying_course_id')
        method_id = ctx.user_data.get('payment_method_id')
        
        if not course_id or not method_id:
            ctx.reply("❌ Qátelik: satıp alıw haqqında maǵlıwmatlar joǵalǵan. Qaytadan baslań.")
            return
        
        course = Course.objects.get(id=course_id)
        payment_method = PaymentMethod.objects.get(id=method_id)
        telegram_user = TelegramUser.objects.get(chat_id=ctx.chat_id)
        
        # Получаем файл с наибольшим разрешением
        photos = ctx.message.get('photo', [])
        if not photos:
            ctx.reply("❌ Foto tabılmadı. Qaytadan urınıp kóriń.")
            return
        
        # Берем фото с наибольшим разрешением
        photo = max(photos, key=lambda p: p.get('file_size', 0))
        file_id = photo['file_id']
        
        # Скачиваем файл
        file_content = bot.download_file(file_id)
        if not file_content:
            ctx.reply("❌ Fotanı júklep alıw múmkin bolmadı. Qaytadan urınıp kóriń.")
            return
        
        # Создаем платеж
        payment = create_payment_record(
            telegram_user, course, payment_method, 
            file_content, 'photo.jpg', ctx.message.get('caption', '')
        )
        
        if payment:
            # Подтверждение пользователю
            success_message = (
                f"✅ <b>Chek qabıllandı!</b>\n\n"
                f"📚 Kurs: {course.name}\n"
                f"💰 Summa: {course.price} sum\n"
                f"💳 Tólem usılı: {payment_method.name}\n\n"
                f"⏳ Siziń tólemińiz administratorǵa tekseriw ushın jiberildi.\n"
                f"Ádette tekseriw 2 saatqa shekem waqıt aladı.\n\n"
                f"Tastıyıqlanǵannan keyin siz kurs gruppasına silteme alasız."
            )
            
            keyboard = KeyboardBuilder.inline_keyboard([[
                {'text': "🏠 Bas menyu", 'callback_data': "back_to_menu"}
            ]])
            
            ctx.reply(success_message, keyboard, parse_mode='HTML')
            ctx.set_state(BotStates.MAIN_MENU)
            
            # Очищаем данные
            ctx.user_data.pop('buying_course_id', None)
            ctx.user_data.pop('payment_method_id', None)
        else:
            ctx.reply("❌ Tólemdi saqlawda qátelik júz berdi. Qaytadan urınıp kóriń.")
        
    except Exception as e:
        logger.error(f"Error processing photo receipt: {e}")
        ctx.reply("Chekti qayta islewde qátelik júz berdi.")

def handle_document_receipt(bot: BotManager, update: dict):
    """Обработчик получения документа чека"""
    ctx = MessageContext(bot, update)
    
    if ctx.user_state != BotStates.WAITING_RECEIPT:
        return
    
    try:
        # Получаем данные о покупке
        course_id = ctx.user_data.get('buying_course_id')
        method_id = ctx.user_data.get('payment_method_id')
        
        if not course_id or not method_id:
            ctx.reply("❌ Qátelik: satıp alıw haqqında maǵlıwmatlar joǵalǵan. Qaytadan baslań.")
            return
        
        course = Course.objects.get(id=course_id)
        payment_method = PaymentMethod.objects.get(id=method_id)
        telegram_user = TelegramUser.objects.get(chat_id=ctx.chat_id)
        
        # Получаем документ
        document = ctx.message.get('document')
        if not document:
            ctx.reply("❌ Hújjet tabılmadı. Qaytadan urınıp kóriń.")
            return
        
        # Проверяем тип файла
        file_name = document.get('file_name', 'receipt')
        mime_type = document.get('mime_type', '')
        file_size = document.get('file_size', 0)
        
        # Ограничиваем размер файла (10 МБ)
        if file_size > 10 * 1024 * 1024:
            ctx.reply("❌ Fayl júdá úlken. Maksimum 10 MB.")
            return
        
        # Проверяем формат
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
        if mime_type not in allowed_types:
            ctx.reply("❌ Qollap-quwatlanbaytuǵın format. PDF, JPG yamasa PNG formatlarınan paydalanıń.")
            return
        
        file_id = document['file_id']
        
        # Скачиваем файл
        file_content = bot.download_file(file_id)
        if not file_content:
            ctx.reply("❌ Fayldı júklep alıw múmkin bolmadı. Qaytadan urınıp kóriń.")
            return
        
        # Создаем платеж
        payment = create_payment_record(
            telegram_user, course, payment_method, 
            file_content, file_name, ctx.message.get('caption', '')
        )
        
        if payment:
            
            # Подтверждение пользователю
            success_message = (
                f"✅ <b>Hújjet qabıllandı!</b>\n\n"
                f"📚 Kurs: {course.name}\n"
                f"💰 Summa: {course.price} sum\n"
                f"💳 Tólem usılı: {payment_method.name}\n"
                f"📄 Fayl: {file_name}\n\n"
                f"⏳ Siziń tólemińiz administratorǵa tekseriw ushın jiberildi.\n"
                f"Ádette tekseriw 2 saatqa shekem waqıt aladı.\n\n"
                f"Tastıyıqlanǵannan keyin siz kurs gruppasına silteme alasız."
            )
            
            keyboard = KeyboardBuilder.inline_keyboard([[
                {'text': "🏠 Bas menyu", 'callback_data': "back_to_menu"}
            ]])
            
            ctx.reply(success_message, keyboard, parse_mode='HTML')
            ctx.set_state(BotStates.MAIN_MENU)
            
            # Очищаем данные
            ctx.user_data.pop('buying_course_id', None)
            ctx.user_data.pop('payment_method_id', None)
        else:
            ctx.reply("❌ Tólemdi saqlawda qátelik júz berdi. Qaytadan urınıp kóriń.")
        
    except Exception as e:
        logger.error(f"Error processing document receipt: {e}")
        ctx.reply("Hújjet qayta islewde qátelik júz berdi.")

def handle_cancel_payment(bot: BotManager, update: dict):
    """Обработчик отмены платежа"""
    ctx = MessageContext(bot, update)
    
    ctx.edit_message(
        "❌ Satıp alıw biykar etildi.\n\n"
        "Siz basqa kurs tańlawıńız yamasa keyinirek qaytıwıńız múmkin.",
        KeyboardBuilder.inline_keyboard([[
            {'text': "📚 Kurslar dizimine", 'callback_data': "back_to_courses"},
            {'text': "🏠 Bas menyu", 'callback_data': "back_to_menu"}
        ]])
    )
    
    ctx.set_state(BotStates.MAIN_MENU)
    # Очищаем данные
    ctx.user_data.pop('buying_course_id', None)
    ctx.user_data.pop('payment_method_id', None)

def create_payment_record(user: TelegramUser, course: Course, payment_method: PaymentMethod, 
                         file_content: bytes, file_name: str, user_comment: str = '') -> Payment:
    """Создать запись платежа в базе данных"""
    try:
        # Создаем уникальное имя файла
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_extension = os.path.splitext(file_name)[1] or '.jpg'
        unique_filename = f"receipt_{user.chat_id}_{timestamp}{file_extension}"
        
        # Создаем файл Django
        django_file = ContentFile(file_content, name=unique_filename)
        
        # Создаем платеж
        payment = Payment.objects.create(
            user=user,
            course=course,
            payment_method=payment_method,
            amount=course.price,
            receipt_file=django_file,
            user_comment=user_comment,
            status='pending'
        )
        
        # Создаем запись уведомления
        PaymentNotification.objects.create(payment=payment)
        
        logger.info(f"Payment created: {payment.id} for user {user.chat_id}")
        return payment
        
    except Exception as e:
        logger.error(f"Error creating payment record: {e}")
        return None

def send_admin_notification(bot: BotManager, payment: Payment):
    """Отправить уведомление администратору о новом платеже"""
    try:
        # Получаем ID администратора из настроек (нужно добавить в .env)
        admin_chat_id = getattr(settings, 'TELEGRAM_ADMIN_CHAT_ID', None)
        
        if not admin_chat_id:
            logger.warning("TELEGRAM_ADMIN_CHAT_ID not configured")
            return
        
        # Формируем сообщение для админа
        message = f"🔔 <b>Jańa tólem!</b>\n\n"
        message += f"👤 Paydalanıwshı: {payment.user.full_name}\n"
        message += f"📱 Telegram: @{payment.user.username or 'kórsetilmegen'}\n"
        message += f"📞 Telefon: {payment.user.phone or 'kórsetilmegen'}\n"
        message += f"🆔 Chat ID: `{payment.user.chat_id}`\n\n"
        message += f"📚 Kurs: {payment.course.name}\n"
        message += f"💰 Summa: {payment.amount} sum\n"
        message += f"💳 Tólem usılı: {payment.payment_method.name}\n\n"
        
        if payment.user_comment:
            message += f"💬 Kommentariy: {payment.user_comment}\n\n"
        
        message += f"🕐 Waqıt: {payment.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        message += f"Tólemdi adminkada tekseriń: /admin/payments/payment/{payment.id}/change/"
        
        # Кнопки для быстрых действий
        buttons = [
            [
                {'text': "✅ Tastıyıqlaw", 'callback_data': f"admin_approve_{payment.id}"},
                {'text': "❌ Biykar etiw", 'callback_data': f"admin_reject_{payment.id}"}
            ],
            [{'text': "📄 Adminkada ashıw", 'callback_data': f"admin_open_{payment.id}"}]
        ]
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        
        # Отправляем сообщение
        bot.send_message(admin_chat_id, message, keyboard, parse_mode='HTML')
        
        # Отправляем файл чека
        if payment.receipt_file:
            try:
                with open(payment.receipt_file.path, 'rb') as f:
                    if payment.is_image:
                        bot.send_photo(
                            admin_chat_id, 
                            f, 
                            caption=f"#{payment.id} tólemi ushın chek"
                        )
                    else:
                        bot.api.send_document(
                            admin_chat_id,
                            f,
                            caption=f"#{payment.id} tólemi ushın chek"
                        )
            except Exception as e:
                logger.error(f"Error sending receipt file to admin: {e}")
        
        # Отмечаем что админ уведомлен
        notification = payment.notification
        notification.admin_notified = True
        notification.save()
        
        logger.info(f"Admin notified about payment {payment.id}")
        
    except Exception as e:
        logger.error(f"Error sending admin notification: {e}")

def send_payment_result_to_user(bot: BotManager, payment: Payment, approved: bool):
    """Отправить результат проверки платежа пользователю"""
    try:
        if approved:
            message = (
                f"✅ <b>Tólem tastıyıqlandı!</b>\n\n"
                f"📚 Kurs: {payment.course.name}\n"
                f"💰 Summa: {payment.amount} sum\n\n"
                f"🎉 Satıp alıwıńız benen qutlıqlaymız!\n\n"
                f"🔗 <b>Kurs gruppasına silteme:</b>\n"
                f"{payment.course.group_link}\n\n"
                f"Gruppaǵa qosılıń hám oqıwdı baslań!\n"
                f"Eger sorawlarıńız bolsa, qollap-quwatlaw xızmetine múrájat etiń."
            )
            
            keyboard = KeyboardBuilder.inline_keyboard([
                [{'text': "🎓 Gruppaǵa ótiw", 'callback_data': f"open_group_{payment.course.id}"}],
                [{'text': "📚 Basqa kurslar", 'callback_data': "back_to_courses"}]
            ])
            keyboard = None
            
            # Отмечаем что ссылка отправлена
            payment.link_sent = True
            payment.save()
            
            # Отмечаем уведомление
            notification = payment.notification
            notification.user_notified_approved = True
            notification.save()
            
        else:
            message = (
                f"❌ <b>Tólem biykar etildi</b>\n\n"
                f"📚 Kurs: {payment.course.name}\n"
                f"💰 Summa: {payment.amount} sum\n\n"
                f"Ókinishke oray, siziń tólemińiz tekseriwden ótpedi.\n\n"
            )
            
            if payment.comment:
                message += f"💬 <b>Administrator kommentariyi:</b>\n{payment.comment}\n\n"
            
            message += (
                f"Eger sorawlarıńız bolsa, qollap-quwatlaw xızmetine múrájat etiń.\n"
                f"Siz taǵı bir márte tólewge urınıp kóriwińizge boladı."
            )
            
            keyboard = KeyboardBuilder.inline_keyboard([
                [{'text': "🔄 Qaytadan urınıp kóriw", 'callback_data': f"buy_{payment.course.id}"}],
                [{'text': "📞 Qollap-quwatlaw", 'callback_data': "support"}]
            ])
            
            # Отмечаем уведомление
            notification = payment.notification
            notification.user_notified_rejected = True
            notification.save()
        
        bot.send_message(payment.user.chat_id, message, keyboard, parse_mode='HTML')
        logger.info(f"Payment result sent to user {payment.user.chat_id}")
        
    except Exception as e:
        logger.error(f"Error sending payment result to user: {e}")
        

def handle_confirm_payment(bot: BotManager, update: dict):
    """Обработчик подтверждения платежа администратором"""
    ctx = MessageContext(bot, update)
    
    try:
        # Извлекаем ID платежа из callback_data
        # Ожидаем формат: "confirm_payment_123" или "admin_approve_123"
        parts = ctx.callback_data.split('_')
        if len(parts) < 3:
            ctx.edit_message("❌ Qátelik: buyrıq formatı nadurıs.")
            return
            
        payment_id = int(parts[-1])  # Берем последний элемент как ID
        
        # Получаем платеж
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            ctx.edit_message("❌ Tólem tabılmadı.")
            return
        
        # Проверяем, что платеж еще не обработан
        if payment.status != 'pending':
            status_text = payment.get_status_display()
            ctx.edit_message(
                f"⚠️ Tólem qayta islenip bolǵan.\n"
                f"Házirgi statusı: {status_text}"
            )
            return
        
        # Подтверждаем платеж
        payment.status = 'approved'
        payment.processed_at = timezone.now()
        payment.save()
        
        # Отправляем ссылку пользователю
        success = send_payment_result_to_user(bot, payment, approved=True)
        
        # Формируем сообщение об успешном подтверждении
        success_message = (
            f"✅ <b>Tólem tastıyıqlandı!</b>\n\n"
            f"👤 Paydalanıwshı: {payment.user.full_name}\n"
            f"📱 @{payment.user.username or 'kórsetilmegen'}\n"
            f"📚 Kurs: {payment.course.name}\n"
            f"💰 Summa: {payment.amount} sum\n"
            f"🕐 Qayta islew waqtı: {payment.processed_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        )
        
        if success:
            success_message += "📤 Gruppaǵa silteme paydalanıwshıǵa jiberildi."
        else:
            success_message += "⚠️ Paydalanıwshıǵa silteme jiberiwde qátelik."
        
        # Кнопки для дальнейших действий
        buttons = [
            [{'text': "📄 Adminkada ashıw", 'callback_data': f"admin_open_{payment.id}"}],
            [{'text': "💬 Paydalanıwshı menen baylanısıw", 'callback_data': f"contact_user_{payment.user.chat_id}"}]
        ]
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        
        ctx.edit_message(success_message, keyboard, parse_mode='HTML')
        
        logger.info(f"Payment {payment.id} approved by admin {ctx.chat_id}")
        
    except ValueError:
        ctx.edit_message("❌ Qátelik: tólem ID nomeri nadurıs.")
    except Exception as e:
        logger.error(f"Error confirming payment: {e}")
        ctx.edit_message("❌ Tólemdi tastıyıqlawda qátelik júz berdi.") 