# payment_handlers.py
# Telegram bot ushın kóp tilli (multi-language) tólem sisteması обработчиклери

import os
import logging
from datetime import datetime
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils import timezone

from bot.bot_manager import BotManager, BotStates, MessageContext, KeyboardBuilder
from bot.models import TelegramUser
from courses.models import Course, PaymentMethod
from payments.models import Payment, PaymentNotification

# Kóp tillilik ushın jańa importlar
from .translations import get_text
from .utils import get_user_language

logger = logging.getLogger(__name__)

def setup_payment_handlers(bot: BotManager):
    """Tólem обработчиклерин sazlaw"""
    
    bot.add_callback_handler('buy_', handle_buy_course)
    bot.add_callback_handler('payment_method_', handle_payment_method_selection)
    bot.add_callback_handler('confirm_payment_', handle_confirm_payment) # Admin ushın
    bot.add_callback_handler('cancel_payment', handle_cancel_payment)
    
    logger.info("Multilingual Payment handlers configured successfully")

def handle_buy_course(bot: BotManager, update: dict):
    """Kurs satıp alıwdı baslaw"""
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    
    try:
        course_id = int(ctx.callback_data.split('_')[1])
        course = Course.objects.get(id=course_id)
        course_name = getattr(course, f'name_{lang}', course.name_qr)

        if not course.is_available:
            ctx.edit_message(
                get_text('course_not_available', lang),
                KeyboardBuilder.inline_keyboard([[{'text': get_text('back_to_courses_button', lang), 'callback_data': "back_to_courses"}]])
            )
            return
        
        telegram_user = TelegramUser.objects.get(chat_id=ctx.chat_id)
        existing_payment = Payment.objects.filter(
            user=telegram_user, course=course, status__in=['approved', 'pending']
        ).first()
        
        if existing_payment:
            if existing_payment.status == 'approved':
                message = get_text('already_bought_course', lang).format(course_name=course_name, group_link=course.group_link)
            else:
                message = get_text('payment_already_pending', lang).format(course_name=course_name, status=existing_payment.get_status_display())
            
            ctx.edit_message(message, KeyboardBuilder.inline_keyboard([[{'text': get_text('back_to_courses_button', lang), 'callback_data': "back_to_courses"}]])
            )
            return
        
        payment_methods = PaymentMethod.objects.filter(is_active=True).order_by('order')
        
        if not payment_methods:
            ctx.edit_message(
                get_text('no_payment_methods_available', lang),
                KeyboardBuilder.inline_keyboard([[{'text': get_text('back_button', lang), 'callback_data': f"course_{course_id}"}]])
            )
            return
        
        if payment_methods.count() == 1:
            fake_update = update.copy()
            fake_update['callback_query'] = fake_update.get('callback_query', {})
            fake_update['callback_query']['data'] = f"payment_method_{course_id}_{payment_methods.first().id}"
            handle_payment_method_selection(bot, fake_update)
            return

        message = get_text('select_payment_method_title', lang).format(course_name=course_name, price=course.price)
        
        buttons = []
        for method in payment_methods:
            method_name = getattr(method, f'name_{lang}', method.name_qr)
            buttons.append([{'text': f"💳 {method_name}", 'callback_data': f"payment_method_{course_id}_{method.id}"}])
        
        buttons.append([{'text': get_text('cancel_button', lang), 'callback_data': f"course_{course_id}"}])
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        ctx.edit_message(message, keyboard)
        ctx.set_state(BotStates.PAYMENT_METHOD)
        ctx.set_data('buying_course_id', course_id)
        
    except Exception as e:
        logger.error(f"Error in buy course: {e}")
        ctx.reply(get_text('error_buy_course', lang))

# payment_handlers.py

def handle_payment_method_selection(bot: BotManager, update: dict):
    """Tólem usılın tańlawdı qayta islew"""
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    
    try:
        parts = ctx.callback_data.split('_')
        course_id = int(parts[2])
        method_id = int(parts[3])
        
        course = Course.objects.get(id=course_id)
        payment_method = PaymentMethod.objects.get(id=method_id)
        
        course_name = course.get_name(lang)
        method_name = payment_method.get_name(lang)

        # --- ÓZGERISLER USı JERDE BASLANADı ---

        # 1. Rekvizitler tekstin bólek jıynaymız
        requisites_info = f"💳 {method_name}\n"
        if payment_method.card_number:
            requisites_info += f"{get_text('payment_method_card_number', lang)} {payment_method.card_number}\n"
        if payment_method.cardholder_name:
            requisites_info += f"{get_text('payment_method_cardholder', lang)} {payment_method.cardholder_name}\n"
        if payment_method.bank_name:
            requisites_info += f"{get_text('payment_method_bank', lang)} {payment_method.bank_name}\n"
        
        method_instructions = payment_method.get_instructions(lang)
        if method_instructions:
            requisites_info += f"{get_text('payment_method_instructions', lang)}\n{method_instructions}"

        # 2. Ulıwma xabardı sol rekvizitler menen birge quramız
        message = get_text('payment_details_title', lang).format(course_name=course_name)
        message += get_text('amount_to_pay', lang).format(price=course.price)
        message += get_text('payment_requisites', lang)
        
        # Eski funkciya shaqırıwı ornına jańa jıynalǵan tekstti qosamız
        message += requisites_info 
        
        message += get_text('important_note', lang)
        message += get_text('important_note_1', lang).format(price=course.price)
        message += get_text('important_note_2', lang)
        message += get_text('important_note_3', lang)
        message += get_text('send_receipt_prompt', lang)
        
        # --- ÓZGERISLER USı JERDE JUWMAQLANADı ---

        buttons = [
            [{'text': get_text('cancel_purchase_button', lang), 'callback_data': "cancel_payment"}],
            [{'text': get_text('back_button', lang), 'callback_data': f"course_{course_id}"}]
        ]
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        
        ctx.edit_message(message, keyboard)
        ctx.set_state(BotStates.WAITING_RECEIPT)
        ctx.set_data('buying_course_id', course_id)
        ctx.set_data('payment_method_id', method_id)
        
    except Exception as e:
        logger.error(f"Error in payment method selection: {e}")
        ctx.reply(get_text('error_payment_method_selection', lang))
        
def handle_photo_receipt(bot: BotManager, update: dict):
    """Chek fotosın qabıl etiw"""
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    
    if ctx.user_state != BotStates.WAITING_RECEIPT: return
    
    try:
        course_id = ctx.user_data.get('buying_course_id')
        method_id = ctx.user_data.get('payment_method_id')
        
        if not course_id or not method_id:
            ctx.reply(get_text('error_purchase_data_lost', lang))
            return
        
        course = Course.objects.get(id=course_id)
        payment_method = PaymentMethod.objects.get(id=method_id)
        telegram_user = TelegramUser.objects.get(chat_id=ctx.chat_id)
        
        photos = ctx.message.get('photo', [])
        if not photos:
            ctx.reply(get_text('error_photo_not_found', lang))
            return
        
        photo = max(photos, key=lambda p: p.get('file_size', 0))
        file_id = photo['file_id']
        file_content = bot.download_file(file_id)
        
        if not file_content:
            ctx.reply(get_text('error_photo_download', lang))
            return
        
        payment = create_payment_record(
            telegram_user, course, payment_method, 
            file_content, 'photo.jpg', ctx.message.get('caption', '')
        )
        
        if payment:
            course_name = getattr(course, f'name_{lang}', course.name_qr)
            method_name = getattr(payment_method, f'name_{lang}', payment_method.name_qr)

            success_message = get_text('receipt_accepted_photo', lang)
            success_message += f"{get_text('course_label', lang)} {course_name}\n"
            success_message += f"{get_text('amount_label', lang)} {course.price} sum\n"
            success_message += f"{get_text('payment_method_label', lang)} {method_name}\n"
            success_message += get_text('payment_pending_admin_review', lang)
            
            keyboard = KeyboardBuilder.inline_keyboard([[{'text': get_text('back_to_menu_button', lang), 'callback_data': "back_to_menu"}]])
            ctx.reply(success_message, keyboard, parse_mode='HTML')
            ctx.set_state(BotStates.MAIN_MENU)
            
            ctx.user_data.pop('buying_course_id', None)
            ctx.user_data.pop('payment_method_id', None)
        else:
            ctx.reply(get_text('error_payment_save', lang))
        
    except Exception as e:
        logger.error(f"Error processing photo receipt: {e}")
        ctx.reply(get_text('error_processing_receipt', lang))

def handle_document_receipt(bot: BotManager, update: dict):
    """Chek hújjetin qabıl etiw"""
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    
    if ctx.user_state != BotStates.WAITING_RECEIPT: return
    
    try:
        course_id = ctx.user_data.get('buying_course_id')
        method_id = ctx.user_data.get('payment_method_id')
        
        if not course_id or not method_id:
            ctx.reply(get_text('error_purchase_data_lost', lang))
            return
        
        course = Course.objects.get(id=course_id)
        payment_method = PaymentMethod.objects.get(id=method_id)
        telegram_user = TelegramUser.objects.get(chat_id=ctx.chat_id)
        
        document = ctx.message.get('document')
        if not document:
            ctx.reply(get_text('error_document_not_found', lang))
            return
        
        file_name = document.get('file_name', 'receipt')
        if document.get('file_size', 0) > 10 * 1024 * 1024:
            ctx.reply(get_text('error_file_too_large', lang))
            return
        
        if document.get('mime_type') not in ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']:
            ctx.reply(get_text('error_unsupported_format', lang))
            return
        
        file_content = bot.download_file(document['file_id'])
        if not file_content:
            ctx.reply(get_text('error_file_download', lang))
            return
        
        payment = create_payment_record(
            telegram_user, course, payment_method, 
            file_content, file_name, ctx.message.get('caption', '')
        )
        
        if payment:
            course_name = getattr(course, f'name_{lang}', course.name_qr)
            method_name = getattr(payment_method, f'name_{lang}', payment_method.name_qr)

            success_message = get_text('receipt_accepted_document', lang)
            success_message += f"{get_text('course_label', lang)} {course_name}\n"
            success_message += f"{get_text('amount_label', lang)} {course.price} sum\n"
            success_message += f"{get_text('payment_method_label', lang)} {method_name}\n"
            success_message += f"{get_text('file_label', lang)} {file_name}\n"
            success_message += get_text('payment_pending_admin_review', lang)
            
            keyboard = KeyboardBuilder.inline_keyboard([[{'text': get_text('back_to_menu_button', lang), 'callback_data': "back_to_menu"}]])
            ctx.reply(success_message, keyboard, parse_mode='HTML')
            ctx.set_state(BotStates.MAIN_MENU)
            
            ctx.user_data.pop('buying_course_id', None)
            ctx.user_data.pop('payment_method_id', None)
        else:
            ctx.reply(get_text('error_payment_save', lang))
        
    except Exception as e:
        logger.error(f"Error processing document receipt: {e}")
        ctx.reply(get_text('error_processing_document', lang))

def handle_cancel_payment(bot: BotManager, update: dict):
    """Tólem processin biykar etiw"""
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    
    ctx.edit_message(
        get_text('purchase_cancelled', lang),
        KeyboardBuilder.inline_keyboard([
            [{'text': get_text('back_to_courses_button', lang), 'callback_data': "back_to_courses"}],
            [{'text': get_text('back_to_menu_button', lang), 'callback_data': "back_to_menu"}]
        ])
    )
    
    ctx.set_state(BotStates.MAIN_MENU)
    ctx.user_data.pop('buying_course_id', None)
    ctx.user_data.pop('payment_method_id', None)

# --- JÁRDEMSHI FUNKCIYALAR (PAYDALANÍWSHÍǴA XABAR JIBERMEYDI) ---

def create_payment_record(user: TelegramUser, course: Course, payment_method: PaymentMethod, 
                         file_content: bytes, file_name: str, user_comment: str = '') -> Payment:
    """Maǵlıwmatlar bazasında tólem jazıwın jaratıw"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_extension = os.path.splitext(file_name)[1] or '.jpg'
        unique_filename = f"receipt_{user.chat_id}_{timestamp}{file_extension}"
        
        django_file = ContentFile(file_content, name=unique_filename)
        
        payment = Payment.objects.create(
            user=user,
            course=course,
            payment_method=payment_method,
            amount=course.price,
            receipt_file=django_file,
            user_comment=user_comment,
            status='pending'
        )
        
        PaymentNotification.objects.create(payment=payment)
        logger.info(f"Payment created: {payment.id} for user {user.chat_id}")
        return payment
        
    except Exception as e:
        logger.error(f"Error creating payment record: {e}")
        return None

def send_admin_notification(bot: BotManager, payment: Payment):
    """Jańa tólem haqqında adminǵa xabar jiberiw (bir tilde)"""
    try:
        admin_chat_id = getattr(settings, 'TELEGRAM_ADMIN_CHAT_ID', None)
        if not admin_chat_id:
            logger.warning("TELEGRAM_ADMIN_CHAT_ID not configured")
            return
        
        # Admin xabarları ushın standart til (mısalı, qaraqalpaqsha)
        course_name_admin = getattr(payment.course, 'name_qr', 'N/A')
        
        message = f"🔔 <b>Jańa tólem!</b>\n\n"
        message += f"👤 Paydalanıwshı: {payment.user.full_name}\n"
        message += f"📱 Telegram: @{payment.user.username or 'kórsetilmegen'}\n"
        message += f"📞 Telefon: {payment.user.phone or 'kórsetilmegen'}\n"
        message += f"🆔 Chat ID: `{payment.user.chat_id}`\n\n"
        message += f"📚 Kurs: {course_name_admin}\n"
        message += f"💰 Summa: {payment.amount} sum\n"
        message += f"💳 Tólem usılı: {payment.payment_method.name}\n\n"
        if payment.user_comment:
            message += f"💬 Kommentariy: {payment.user_comment}\n\n"
        message += f"🕐 Waqıt: {payment.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        message += f"Tólemdi adminkada tekseriń: /admin/payments/payment/{payment.id}/change/"
        
        buttons = [
            [{'text': "✅ Tastıyıqlaw", 'callback_data': f"admin_approve_{payment.id}"},
             {'text': "❌ Biykar etiw", 'callback_data': f"admin_reject_{payment.id}"}]
        ]
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        bot.send_message(admin_chat_id, message, keyboard, parse_mode='HTML')
        
        if payment.receipt_file:
            # ... (chek jiberiw kodı ózgerissiz qaladı) ...
            pass
        
        notification = payment.notification
        notification.admin_notified = True
        notification.save()
        logger.info(f"Admin notified about payment {payment.id}")
        
    except Exception as e:
        logger.error(f"Error sending admin notification: {e}")

# --- PAYDALANÍWSHÍǴA NÁTIYJE JIBERIW ---

def send_payment_result_to_user(bot: BotManager, payment: Payment, approved: bool):
    """Tólem nátiyjesin paydalanıwshıǵa jiberiw"""
    lang = get_user_language(payment.user.chat_id)
    course_name = getattr(payment.course, f'name_{lang}', payment.course.name_qr)
    
    try:
        if approved:
            message = get_text('payment_approved_title', lang)
            message += f"{get_text('course_label', lang)} {course_name}\n"
            message += f"{get_text('amount_label', lang)} {payment.amount} sum\n\n"
            message += get_text('congratulations_on_purchase', lang)
            message += get_text('group_link_message', lang).format(group_link=payment.course.group_link)
            message += get_text('join_group_and_start', lang)
            
            keyboard = KeyboardBuilder.inline_keyboard([
                [{'text': get_text('other_courses_button', lang), 'callback_data': "back_to_courses"}]
            ])
            
            payment.link_sent = True
            payment.save()
            payment.notification.user_notified_approved = True
            payment.notification.save()
            
        else: # Biykar etilgen bolsa
            message = get_text('payment_rejected_title', lang)
            message += f"{get_text('course_label', lang)} {course_name}\n"
            message += f"{get_text('amount_label', lang)} {payment.amount} sum\n\n"
            message += get_text('payment_rejected_body', lang)
            
            if payment.comment:
                message += get_text('admin_comment_message', lang).format(comment=payment.comment)
            
            message += get_text('if_questions_contact_support', lang)
            
            keyboard = KeyboardBuilder.inline_keyboard([
                [{'text': get_text('retry_payment_button', lang), 'callback_data': f"buy_{payment.course.id}"}],
                [{'text': get_text('support_button', lang), 'callback_data': "support"}]
            ])
            
            payment.notification.user_notified_rejected = True
            payment.notification.save()
        
        bot.send_message(payment.user.chat_id, message, keyboard, parse_mode='HTML')
        logger.info(f"Payment result sent to user {payment.user.chat_id}")
        
    except Exception as e:
        logger.error(f"Error sending payment result to user: {e}")

# --- ADMIN USHÍN CALLBACK HANDLER (ÓZGERISSZ QALADÍ) ---
def handle_confirm_payment(bot: BotManager, update: dict):
    """Tólem tastıyıqlanıwın admin tárepinen qayta islew (bir tilde)"""
    ctx = MessageContext(bot, update)
    try:
        payment_id = int(ctx.callback_data.split('_')[-1])
        payment = Payment.objects.get(id=payment_id)
        
        if payment.status != 'pending':
            ctx.edit_message(f"⚠️ Tólem qayta islenip bolǵan. Házirgi statusı: {payment.get_status_display()}")
            return
        
        payment.approve() # Approve ózi processed_at hám status-tı ózgertedi dep esaplaymız
        success = send_payment_result_to_user(bot, payment, approved=True)
        
        success_message = f"✅ <b>Tólem tastıyıqlandı!</b>\n\n"
        success_message += f"👤 Paydalanıwshı: {payment.user.full_name}\n"
        success_message += f"📚 Kurs: {payment.course.name}\n\n"
        if success:
            success_message += "📤 Gruppaǵa silteme paydalanıwshıǵa jiberildi."
        else:
            success_message += "⚠️ Paydalanıwshıǵa silteme jiberiwde qátelik."
        
        ctx.edit_message(success_message, parse_mode='HTML')
        logger.info(f"Payment {payment.id} approved by admin {ctx.chat_id}")
        
    except (ValueError, Payment.DoesNotExist) as e:
        ctx.edit_message("❌ Qátelik: Tólem tabılmadı yamasa ID nadurıs.")
    except Exception as e:
        logger.error(f"Error confirming payment: {e}")
        ctx.edit_message("❌ Tólemdi tastıyıqlawda qátelik júz berdi.")