# bot_handlers_simple.py
# Telegram bot ushın kóp tilli (multi-language) обработчиклер

import logging
from django.utils import timezone
from bot.bot_manager import BotManager, BotStates, MessageContext, KeyboardBuilder
from bot.models import TelegramUser, UserState, InfoPage
from courses.models import Course
from bot.payment_handlers import (
    setup_payment_handlers, handle_photo_receipt, handle_document_receipt,
    send_payment_result_to_user
)
# Kóp tillilik ushın jańa import
from .translations import get_text

logger = logging.getLogger(__name__)


from .utils import get_user_language

# --- TIYKARǴÍ HANDLERLAR ---

def setup_bot_handlers(bot: BotManager):
    """Barlıq bot обработчиклерин sazlaw"""
    
    # Buyrıqlar
    bot.add_command_handler('start', handle_start_command)
    bot.add_command_handler('cancel', handle_cancel_command)
    bot.add_command_handler('help', handle_help_command)
    
    # Tekstlik túymelerdi qayta islew ushın ulıwma handler
    # ESKI HANDLERLARDI ALıP TASLAŃ: bot.add_text_handler('📚 Kurslar', ...)
    # bot.add_message_handler(handle_text_router, filters={'text': True})
    
    bot.add_text_handler(get_text('courses_button', 'qr'), handle_courses_button)
    bot.add_text_handler(get_text('courses_button', 'uz'), handle_courses_button)
    bot.add_text_handler(get_text('about_button', 'qr'), handle_about_button)
    bot.add_text_handler(get_text('about_button', 'uz'), handle_about_button)
    bot.add_text_handler(get_text('support_button', 'qr'), handle_support_button)
    bot.add_text_handler(get_text('support_button', 'uz'), handle_support_button)
    
    # Kontakt
    bot.set_contact_handler(handle_contact)
    
    # Callback обработчиклер
    bot.add_callback_handler('set_lang_', handle_language_selection) # Til tańlaw ushın jańa
    bot.add_callback_handler('course_', handle_course_details)
    bot.add_callback_handler('back_to_courses', handle_back_to_courses)
    bot.add_callback_handler('back_to_menu', handle_back_to_menu)
    
    # Foto hám hújjetler
    bot.set_photo_handler(handle_photo)
    bot.set_document_handler(handle_document)
    
    # Tólem обработчиклерин sazlaw
    setup_payment_handlers(bot)
    
    logger.info("All multilingual bot handlers configured successfully")

def handle_start_command(bot: BotManager, update: dict):
    """/start buyrıǵın qayta islew"""
    ctx = MessageContext(bot, update)
    
    try:
        telegram_user, created = TelegramUser.objects.get_or_create(
            chat_id=ctx.chat_id,
            defaults={
                'username': ctx.user.get('username'),
                'first_name': ctx.user.get('first_name', ''),
                'last_name': ctx.user.get('last_name', ''),
            }
        )
        
        if not created:
            telegram_user.username = ctx.user.get('username') or telegram_user.username
            telegram_user.first_name = ctx.user.get('first_name', '') or telegram_user.first_name
            telegram_user.last_name = ctx.user.get('last_name', '') or telegram_user.last_name
            telegram_user.save()
        
        telegram_user.update_activity()
        
        # 1. Dáslep tildi tekseriw
        # if not telegram_user.language:
        buttons = [
            [{'text': get_text('language_chosen_button', 'qr'), 'callback_data': "set_lang_qr"}],
            [{'text': get_text('language_chosen_button', 'uz'), 'callback_data': "set_lang_uz"}]
        ]
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        ctx.reply(get_text('welcome_prompt_language', 'qr'), reply_markup=keyboard)
        ctx.set_state(BotStates.WAITING_LANGUAGE) # BotStates-qa qosıwdı umıtpań!
        return

        # lang = telegram_user.language
        # # 2. Tilden keyin nomerdi tekseriw
        # if not telegram_user.phone:
        #     keyboard = KeyboardBuilder.reply_keyboard(
        #         [[get_text('request_contact_button', lang)]], 
        #         one_time_keyboard=True
        #     )
        #     ctx.reply(get_text('welcome_after_lang', lang), reply_markup=keyboard)
        #     ctx.set_state(BotStates.WAITING_CONTACT)
        # else:
        #     show_main_menu(ctx)
        #     ctx.set_state(BotStates.MAIN_MENU)
    
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        ctx.reply(get_text('error_start_command', 'qr')) # Baslanǵısh qátelik ushın standart til

def handle_language_selection(bot: BotManager, update: dict):
    """Til tańlawdı qayta islew"""
    ctx = MessageContext(bot, update)
    try:
        lang_code = ctx.callback_data.split('_')[2]
        if lang_code not in ['qr', 'uz']: return

        user = TelegramUser.objects.get(chat_id=ctx.chat_id)
        user.language = lang_code
        user.save()
        
        ctx.edit_message(get_text('language_selected', lang_code)) # Til tańlaw xabarın óshiriw
        
        # Nomer soraw basqıshına ótiw
        if not user.phone:
            keyboard = KeyboardBuilder.reply_keyboard(
                # [[get_text('request_contact_button', lang_code)]],
                [[{'text': get_text('request_contact_button', lang_code), 'request_contact': True}]], 
                one_time_keyboard=True
            )
            ctx.reply(get_text('welcome_after_lang', lang_code), reply_markup=keyboard)
            ctx.set_state(BotStates.WAITING_CONTACT)
        else:
            show_main_menu(ctx)
            ctx.set_state(BotStates.MAIN_MENU)
            
    except Exception as e:
        logger.error(f"Error handling language selection: {e}")

def handle_contact(bot: BotManager, update: dict):
    """Kontakt alıwdı qayta islew"""
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    
    try:
        contact = ctx.message.get('contact')
        if contact and contact.get('user_id') == ctx.user.get('id'):
            user = TelegramUser.objects.get(chat_id=ctx.chat_id)
            user.phone = contact.get('phone_number')
            user.first_name = contact.get('first_name') or user.first_name
            user.last_name = contact.get('last_name') or user.last_name
            user.save()
            
            logger.info(f"Contact received from user {ctx.chat_id}: {user.phone}")
            
            ctx.reply(get_text('contact_saved', lang))
            show_main_menu(ctx)
            ctx.set_state(BotStates.MAIN_MENU)
        else:
            keyboard = KeyboardBuilder.reply_keyboard(
                [[get_text('request_contact_button', lang)]], 
                one_time_keyboard=True
            )
            ctx.reply(get_text('error_not_your_contact', lang), reply_markup=keyboard)
    
    except Exception as e:
        logger.error(f"Error handling contact: {e}")
        ctx.reply(get_text('error_contact_save', lang))

# --- MENYU TÚYME HANDLERLERI ---

def handle_courses_button(bot: BotManager, update: dict):
    """'Kurslar' túymesin qayta islew"""
    ctx = MessageContext(bot, update)
    show_courses_list(ctx)

def handle_about_button(bot: BotManager, update: dict):
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    try:
        page = InfoPage.objects.get(key="about")
        # Keleshekte InfoPage modelin de kóp tilli qılıw múmkin (mısalı, content_qr, content_uz)
        if lang == 'qr':
            ctx.reply(f"{page.content_qr}", parse_mode='HTML')
        else:
            ctx.reply(f"{page.content_uz}", parse_mode='HTML')
    except InfoPage.DoesNotExist:
        ctx.reply(get_text('info_not_found', lang))

def handle_support_button(bot: BotManager, update: dict):
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    try:
        page = InfoPage.objects.get(key="support")
        if lang == 'qr':
            ctx.reply(f"{page.content_qr}", parse_mode='HTML')
        else:
            ctx.reply(f"{page.content_uz}", parse_mode='HTML')
    except InfoPage.DoesNotExist:
        ctx.reply(get_text('support_info_not_found', lang))

# --- KURSLAR MENEN ISLEW ---

def handle_course_details(bot: BotManager, update: dict):
    """Kurs haqqında tolıq maǵlıwmattı kórsetiw"""
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    
    try:
        course_id = int(ctx.callback_data.split('_')[1])
        course = Course.objects.get(id=course_id)
        
        # Kurs atı hám sıpatlamasın paydalanıwshı tilinde alıw (Course modelin ózgertiw kerek)
        course_name = getattr(course, f'name_{lang}', course.name_qr)
        course_description = getattr(course, f'description_{lang}', course.description_qr)

        message = get_text('course_details_header', lang).format(
            course_name=course_name, course_description=course_description
        )
        
        if course.discount_percentage > 0:
            message += get_text('price_label', lang) + " "
            message += get_text('old_price_label', lang).format(old_price=course.old_price, price=course.price)
            message += " " + get_text('discount_label', lang).format(discount=course.discount_percentage)
        else:
            message += get_text('price_label', lang) + " "
            message += get_text('current_price_label', lang).format(price=course.price)
        
        if course.max_students:
            current_students = course.current_students_count
            message += get_text('taken_slots', lang).format(current=current_students, max=course.max_students)
            if not course.is_available:
                message += get_text('no_slots_left', lang)
            else:
                message += get_text('free_slots', lang).format(free=course.max_students - current_students)
        
        buttons = []
        if course.is_available:
            buttons.append([{'text': get_text('buy_button', lang).format(price=course.price), 'callback_data': f"buy_{course.id}"}])
        
        buttons.extend([
            [{'text': get_text('back_to_courses_button', lang), 'callback_data': "back_to_courses"}],
            [{'text': get_text('back_to_menu_button', lang), 'callback_data': "back_to_menu"}]
        ])
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        ctx.edit_message(message, keyboard)
        ctx.set_state(BotStates.COURSE_DETAILS)
        ctx.set_data('selected_course_id', course_id)
    
    except Exception as e:
        logger.error(f"Error showing course details: {e}")
        ctx.reply(get_text('error_loading_course_details', lang))

def handle_back_to_courses(bot: BotManager, update: dict):
    """Kurslar dizimine qaytıw"""
    ctx = MessageContext(bot, update)
    show_courses_list(ctx, edit_message=True)

def handle_back_to_menu(bot: BotManager, update: dict):
    """Bas menyuǵa qaytıw"""
    ctx = MessageContext(bot, update)
    try:
        bot.api.delete_message(ctx.chat_id, ctx.message['message_id'])
    except:
        pass
    show_main_menu(ctx)
    ctx.set_state(BotStates.MAIN_MENU)

# --- BASQA BUYRÍQLAR HÁM HANDLERLAR ---

def handle_cancel_command(bot: BotManager, update: dict):
    """/cancel buyrıǵın qayta islew"""
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    
    ctx.reply(get_text('returning_to_main_menu', lang))
    show_main_menu(ctx)
    ctx.set_state(BotStates.MAIN_MENU)
    
    ctx.user_data.pop('buying_course_id', None)
    ctx.user_data.pop('payment_method_id', None)

def handle_help_command(bot: BotManager, update: dict):
    """/help buyrıǵın qayta islew"""
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    ctx.reply(get_text('help_text', lang), parse_mode='HTML')

def handle_photo(bot: BotManager, update: dict):
    """Foto qabıl etiw"""
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    
    if ctx.user_state == BotStates.WAITING_RECEIPT:
        handle_photo_receipt(bot, update)
    else:
        ctx.reply(get_text('photo_received_outside_payment', lang))

def handle_document(bot: BotManager, update: dict):
    """Hújjet qabıl etiw"""
    ctx = MessageContext(bot, update)
    lang = get_user_language(ctx.chat_id)
    
    if ctx.user_state == BotStates.WAITING_RECEIPT:
        handle_document_receipt(bot, update)
    else:
        ctx.reply(get_text('document_received_outside_payment', lang))

# --- KÓRSETIW FUNKCIYALARÍ (SHOW FUNCTIONS) ---

def show_main_menu(ctx: MessageContext):
    """Bas menyudı kórsetiw"""
    lang = get_user_language(ctx.chat_id)
    keyboard = KeyboardBuilder.reply_keyboard([
        [get_text('courses_button', lang)],
        [get_text('about_button', lang), get_text('support_button', lang)]
    ])
    ctx.reply(get_text('main_menu_title', lang), reply_markup=keyboard, parse_mode='HTML')

def show_courses_list(ctx: MessageContext, edit_message: bool = False):
    """Kurslar dizimin kórsetiw"""
    lang = get_user_language(ctx.chat_id)
    try:
        courses = Course.objects.filter(is_active=True).order_by('order')
        
        if not courses:
            message = get_text('no_courses_yet', lang)
            if edit_message: ctx.edit_message(message)
            else: ctx.reply(message)
            return
        
        buttons = []
        for course in courses:
            # Kurs atın paydalanıwshı tilinde alıw
            course_name = getattr(course, f'name_{lang}', course.name_qr)
            button_text = f"📚 {course_name}"
            if course.discount_percentage > 0:
                button_text += f" (-{course.discount_percentage}%)"
            
            buttons.append([{'text': button_text, 'callback_data': f"course_{course.id}"}])
        
        buttons.append([{'text': get_text('back_to_menu_button', lang), 'callback_data': "back_to_menu"}])
        
        keyboard = KeyboardBuilder.inline_keyboard(buttons)
        message = get_text('courses_list_title', lang)
        
        if edit_message:
            ctx.edit_message(message, keyboard)
        else:
            ctx.reply(message, keyboard, parse_mode='HTML')
        
        ctx.set_state(BotStates.COURSE_SELECTION)
    
    except Exception as e:
        logger.error(f"Error showing courses: {e}")
        ctx.reply(get_text('error_loading_courses', lang))

# --- ADMIN FUNKCIYALARÍ ---
# Bul funkciyalar paydalanıwshıǵa tikkeley xabar jibermeytuǵınlıqtan, ózgerissiz qaladı.
# Xabar jiberiw logikası payment_handlers.py faylındaǵı send_payment_result_to_user ishinde.

def handle_admin_approve_payment(bot: BotManager, payment_id: int):
    """Tólem tastıyıqlanıwın qayta islew"""
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
    """Tólem biykar etiliwin qayta islew"""
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