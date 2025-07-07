# bot/bot_handlers.py

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, filters, ContextTypes
)
from django.conf import settings
from asgiref.sync import sync_to_async
from .models import TelegramUser, UserState
from courses.models import Course
from decimal import Decimal

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния разговора
(
    START,
    WAITING_CONTACT,
    MAIN_MENU,
    COURSE_SELECTION,
    COURSE_DETAILS,
    PAYMENT_METHOD,
    WAITING_RECEIPT,
) = range(7)

class BotHandlers:
    """Класс с обработчиками бота"""
    
    @staticmethod
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработчик команды /start"""
        try:
            user = update.effective_user
            chat_id = update.effective_chat.id
            
            logger.info(f"Пользователь {user.id} ({user.username}) начал диалог")
            
            # Проверяем, существует ли пользователь в базе
            telegram_user, created = await sync_to_async(TelegramUser.objects.get_or_create)(
                chat_id=chat_id,
                defaults={
                    'username': user.username,
                    'first_name': user.first_name or '',
                    'last_name': user.last_name or '',
                }
            )
            
            if created:
                logger.info(f"Создан новый пользователь: {telegram_user}")
                
            # Обновляем активность
            await sync_to_async(telegram_user.update_activity)()
            
            # Если у пользователя нет номера телефона, запрашиваем его
            if not telegram_user.phone:
                await update.message.reply_text(
                    "🎓 Добро пожаловать в бот для покупки курсов!\n\n"
                    "Я помогу вам выбрать и купить подходящий курс.\n"
                    "Для начала поделитесь своим номером телефона.",
                    reply_markup=get_contact_keyboard()
                )
                return WAITING_CONTACT
            else:
                # Если контакт уже есть, переходим к главному меню
                await show_main_menu(update, context)
                return MAIN_MENU
                
        except Exception as e:
            logger.error(f"Ошибка в start_command: {e}")
            await update.message.reply_text(
                "Произошла ошибка. Попробуйте еще раз /start"
            )
            return ConversationHandler.END

    @staticmethod
    async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработчик получения контакта"""
        try:
            contact = update.message.contact
            chat_id = update.effective_chat.id
            
            if contact and contact.user_id == update.effective_user.id:
                # Обновляем информацию о пользователе
                telegram_user = await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)
                telegram_user.phone = contact.phone_number
                telegram_user.first_name = contact.first_name or telegram_user.first_name
                telegram_user.last_name = contact.last_name or telegram_user.last_name
                await sync_to_async(telegram_user.save)()
                
                logger.info(f"Получен контакт от пользователя {chat_id}: {contact.phone_number}")
                
                await update.message.reply_text(
                    "✅ Спасибо! Ваш номер телефона сохранен.\n\n"
                    "Теперь вы можете выбрать курс:",
                    reply_markup=get_main_menu_keyboard()
                )
                
                await show_main_menu(update, context)
                return MAIN_MENU
            else:
                await update.message.reply_text(
                    "❌ Пожалуйста, поделитесь именно своим номером телефона.",
                    reply_markup=get_contact_keyboard()
                )
                return WAITING_CONTACT
                
        except Exception as e:
            logger.error(f"Ошибка в handle_contact: {e}")
            await update.message.reply_text(
                "Произошла ошибка при сохранении контакта. Попробуйте еще раз."
            )
            return WAITING_CONTACT

    @staticmethod
    async def show_courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Показать список курсов"""
        try:
            # Получаем активные курсы
            courses = await sync_to_async(list)(
                Course.objects.filter(is_active=True).order_by('order', 'name')
            )
            
            if not courses:
                await update.message.reply_text(
                    "😔 К сожалению, сейчас нет доступных курсов.\n"
                    "Попробуйте позже.",
                    reply_markup=get_main_menu_keyboard()
                )
                return MAIN_MENU
            
            # Создаем клавиатуру с курсами
            keyboard = []
            for course in courses:
                button_text = f"📚 {course.name}"
                if course.discount_percentage > 0:
                    button_text += f" (-{course.discount_percentage}%)"
                
                keyboard.append([
                    InlineKeyboardButton(
                        button_text,
                        callback_data=f"course_{course.id}"
                    )
                ])
            
            keyboard.append([
                InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")
            ])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "📚 **Доступные курсы:**\n\n"
                "Выберите курс, чтобы узнать подробности и купить:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            return COURSE_SELECTION
            
        except Exception as e:
            logger.error(f"Ошибка в show_courses: {e}")
            await update.message.reply_text(
                "Произошла ошибка при загрузке курсов.",
                reply_markup=get_main_menu_keyboard()
            )
            return MAIN_MENU

    @staticmethod
    async def course_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Показать детали курса"""
        try:
            query = update.callback_query
            await query.answer()
            
            course_id = int(query.data.split('_')[1])
            course = await sync_to_async(Course.objects.get)(id=course_id)
            
            # Формируем сообщение с информацией о курсе
            message = f"📚 **{course.name}**\n\n"
            message += f"{course.get_display_description()}\n\n"
            
            # Цена и скидка
            if course.discount_percentage > 0:
                message += f"💰 Цена: ~~{course.old_price}~~ **{course.price} руб** "
                message += f"🔥 **(-{course.discount_percentage}%)**\n\n"
            else:
                message += f"💰 Цена: **{course.price} руб**\n\n"
            
            # Информация о доступности
            if course.max_students:
                current_students = course.current_students_count
                message += f"👥 Мест занято: {current_students}/{course.max_students}\n"
                
                if not course.is_available:
                    message += "❌ **Мест больше нет**\n\n"
                else:
                    message += f"✅ Доступно мест: {course.max_students - current_students}\n\n"
            
            # Кнопки
            keyboard = []
            
            if course.is_available:
                keyboard.append([
                    InlineKeyboardButton(
                        f"💳 Купить за {course.price} руб",
                        callback_data=f"buy_{course.id}"
                    )
                ])
            
            keyboard.extend([
                [InlineKeyboardButton("◀️ К списку курсов", callback_data="back_to_courses")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_menu")]
            ])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            # Сохраняем ID курса в контексте
            context.user_data['selected_course_id'] = course_id
            
            return COURSE_DETAILS
            
        except Exception as e:
            logger.error(f"Ошибка в course_details: {e}")
            await query.message.reply_text(
                "Произошла ошибка при загрузке информации о курсе."
            )
            return COURSE_SELECTION

    @staticmethod
    async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработчик текстовых сообщений"""
        try:
            text = update.message.text
            chat_id = update.effective_chat.id
            
            # Обновляем активность пользователя
            try:
                telegram_user = await sync_to_async(TelegramUser.objects.get)(chat_id=chat_id)
                await sync_to_async(telegram_user.update_activity)()
            except TelegramUser.DoesNotExist:
                # Если пользователь не найден, начинаем заново
                return await BotHandlers.start_command(update, context)
            
            if text == "📚 Курсы":
                return await BotHandlers.show_courses(update, context)
            elif text == "ℹ️ О нас":
                await update.message.reply_text(
                    "📖 **О нас**\n\n"
                    "Мы предлагаем качественные онлайн-курсы по программированию.\n\n"
                    "🎯 Наши преимущества:\n"
                    "• Практические задания\n"
                    "• Поддержка преподавателей\n"
                    "• Сертификаты о прохождении\n"
                    "• Доступ к закрытым группам\n\n"
                    "📞 Остались вопросы? Напишите @support",
                    reply_markup=get_main_menu_keyboard(),
                    parse_mode='Markdown'
                )
                return MAIN_MENU
            elif text == "📞 Поддержка":
                await update.message.reply_text(
                    "📞 **Поддержка**\n\n"
                    "Если у вас есть вопросы, обращайтесь:\n\n"
                    "👨‍💻 Telegram: @support\n"
                    "📧 Email: support@example.com\n"
                    "🕐 Время работы: 9:00 - 21:00 (МСК)\n\n"
                    "Мы обязательно вам поможем!",
                    reply_markup=get_main_menu_keyboard(),
                    parse_mode='Markdown'
                )
                return MAIN_MENU
            else:
                await update.message.reply_text(
                    "❓ Не понимаю эту команду. Используйте кнопки меню:",
                    reply_markup=get_main_menu_keyboard()
                )
                return MAIN_MENU
                
        except Exception as e:
            logger.error(f"Ошибка в handle_text_messages: {e}")
            await update.message.reply_text(
                "Произошла ошибка. Попробуйте еще раз.",
                reply_markup=get_main_menu_keyboard()
            )
            return MAIN_MENU

    @staticmethod
    async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработчик callback запросов"""
        try:
            query = update.callback_query
            await query.answer()
            
            data = query.data
            
            if data.startswith("course_"):
                return await BotHandlers.course_details(update, context)
            elif data.startswith("buy_"):
                # Обработка покупки будет добавлена в следующем этапе
                await query.edit_message_text(
                    "💳 Функция покупки будет добавлена в следующем этапе разработки.\n\n"
                    "Пока вы можете просмотреть другие курсы.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("◀️ К списку курсов", callback_data="back_to_courses")
                    ]])
                )
                return COURSE_DETAILS
            elif data == "back_to_courses":
                # Показываем список курсов заново
                courses = await sync_to_async(list)(
                    Course.objects.filter(is_active=True).order_by('order', 'name')
                )
                
                keyboard = []
                for course in courses:
                    button_text = f"📚 {course.name}"
                    if course.discount_percentage > 0:
                        button_text += f" (-{course.discount_percentage}%)"
                    
                    keyboard.append([
                        InlineKeyboardButton(button_text, callback_data=f"course_{course.id}")
                    ])
                
                keyboard.append([
                    InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_menu")
                ])
                
                await query.edit_message_text(
                    "📚 **Доступные курсы:**\n\n"
                    "Выберите курс, чтобы узнать подробности и купить:",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode='Markdown'
                )
                return COURSE_SELECTION
            elif data == "back_to_menu":
                await query.delete_message()
                await show_main_menu_via_message(query.message, context)
                return MAIN_MENU
                
        except Exception as e:
            logger.error(f"Ошибка в handle_callback_query: {e}")
            await query.message.reply_text(
                "Произошла ошибка. Попробуйте еще раз."
            )
            return MAIN_MENU

    @staticmethod
    async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Обработчик команды /cancel"""
        await update.message.reply_text(
            "🏠 Возвращаемся в главное меню.",
            reply_markup=get_main_menu_keyboard()
        )
        await show_main_menu(update, context)
        return MAIN_MENU

# Вспомогательные функции

def get_contact_keyboard():
    """Клавиатура для запроса контакта"""
    keyboard = [
        [KeyboardButton("📱 Поделиться номером", request_contact=True)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_main_menu_keyboard():
    """Основная клавиатура меню"""
    keyboard = [
        ["📚 Курсы"],
        ["ℹ️ О нас", "📞 Поддержка"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню"""
    await update.message.reply_text(
        "🏠 **Главное меню**\n\n"
        "Выберите действие:",
        reply_markup=get_main_menu_keyboard(),
        parse_mode='Markdown'
    )

async def show_main_menu_via_message(message, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню через объект сообщения"""
    await message.reply_text(
        "🏠 **Главное меню**\n\n"
        "Выберите действие:",
        reply_markup=get_main_menu_keyboard(),
        parse_mode='Markdown'
    )

def get_conversation_handler():
    """Создание ConversationHandler для бота"""
    return ConversationHandler(
        entry_points=[CommandHandler('start', BotHandlers.start_command)],
        states={
            WAITING_CONTACT: [
                MessageHandler(filters.CONTACT, BotHandlers.handle_contact),
                MessageHandler(filters.TEXT & ~filters.COMMAND, 
                             lambda u, c: u.message.reply_text(
                                 "Пожалуйста, поделитесь номером телефона, используя кнопку ниже.",
                                 reply_markup=get_contact_keyboard()
                             ))
            ],
            MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, BotHandlers.handle_text_messages),
                CallbackQueryHandler(BotHandlers.handle_callback_query)
            ],
            COURSE_SELECTION: [
                CallbackQueryHandler(BotHandlers.handle_callback_query),
                MessageHandler(filters.TEXT & ~filters.COMMAND, BotHandlers.handle_text_messages)
            ],
            COURSE_DETAILS: [
                CallbackQueryHandler(BotHandlers.handle_callback_query),
                MessageHandler(filters.TEXT & ~filters.COMMAND, BotHandlers.handle_text_messages)
            ],
        },
        fallbacks=[
            CommandHandler('cancel', BotHandlers.cancel_command),
            CommandHandler('start', BotHandlers.start_command)
        ],
        allow_reentry=True
    )

def setup_bot_application():
    """Настройка приложения бота"""
    if not settings.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не настроен")
    
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(get_conversation_handler())
    
    logger.info("Приложение бота настроено успешно")
    return application