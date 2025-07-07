# bot_manager.py
# Простая система управления Telegram ботом без внешних библиотек

import time
import logging
import json
from typing import Dict, Callable, Any, Optional
from .telegram_api import TelegramAPI, KeyboardBuilder

logger = logging.getLogger(__name__)

# Состояния бота
class BotStates:
    START = "start"
    WAITING_CONTACT = "waiting_contact"
    MAIN_MENU = "main_menu"
    COURSE_SELECTION = "course_selection"
    COURSE_DETAILS = "course_details"
    PAYMENT_METHOD = "payment_method"
    WAITING_RECEIPT = "waiting_receipt"

class BotManager:
    """Простой менеджер для Telegram бота"""
    
    def __init__(self, token: str):
        self.api = TelegramAPI(token)
        self.handlers = {
            'command': {},      # Обработчики команд /start, /help и т.д.
            'text': {},         # Обработчики текстовых сообщений
            'callback': {},     # Обработчики callback запросов
            'contact': None,    # Обработчик контактов
            'photo': None,      # Обработчик фото
            'document': None,   # Обработчик документов
        }
        self.user_states = {}   # Состояния пользователей {chat_id: state}
        self.user_data = {}     # Данные пользователей {chat_id: data}
        self.last_update_id = 0
        self.running = False
    
    def add_command_handler(self, command: str, handler: Callable):
        """Добавить обработчик команды"""
        self.handlers['command'][command] = handler
    
    def add_text_handler(self, text: str, handler: Callable):
        """Добавить обработчик текста"""
        self.handlers['text'][text] = handler
    
    def add_callback_handler(self, callback_data: str, handler: Callable):
        """Добавить обработчик callback"""
        self.handlers['callback'][callback_data] = handler
    
    def set_contact_handler(self, handler: Callable):
        """Установить обработчик контактов"""
        self.handlers['contact'] = handler
    
    def set_photo_handler(self, handler: Callable):
        """Установить обработчик фото"""
        self.handlers['photo'] = handler
    
    def set_document_handler(self, handler: Callable):
        """Установить обработчик документов"""
        self.handlers['document'] = handler
    
    def get_user_state(self, chat_id: int) -> str:
        """Получить состояние пользователя"""
        return self.user_states.get(chat_id, BotStates.START)
    
    def set_user_state(self, chat_id: int, state: str):
        """Установить состояние пользователя"""
        self.user_states[chat_id] = state
        logger.info(f"User {chat_id} state changed to: {state}")
    
    def get_user_data(self, chat_id: int) -> Dict:
        """Получить данные пользователя"""
        if chat_id not in self.user_data:
            self.user_data[chat_id] = {}
        return self.user_data[chat_id]
    
    def set_user_data(self, chat_id: int, key: str, value: Any):
        """Установить данные пользователя"""
        if chat_id not in self.user_data:
            self.user_data[chat_id] = {}
        self.user_data[chat_id][key] = value
    
    def process_update(self, update: Dict):
        """Обработать одно обновление"""
        try:
            # Обработка сообщений
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                user = message['from']
                
                logger.info(f"Message from {user.get('username', user.get('first_name', 'Unknown'))} ({chat_id})")
                
                # Команды
                if 'text' in message and message['text'].startswith('/'):
                    command = message['text'][1:]  # Убираем /
                    if command in self.handlers['command']:
                        self.handlers['command'][command](self, update)
                        return
                
                # Контакт
                if 'contact' in message:
                    if self.handlers['contact']:
                        self.handlers['contact'](self, update)
                        return
                
                # Фото
                if 'photo' in message:
                    if self.handlers['photo']:
                        self.handlers['photo'](self, update)
                        return
                
                # Документ
                if 'document' in message:
                    if self.handlers['document']:
                        self.handlers['document'](self, update)
                        return
                
                # Текстовые сообщения
                if 'text' in message:
                    text = message['text']
                    
                    # Проверяем конкретные обработчики текста
                    if text in self.handlers['text']:
                        self.handlers['text'][text](self, update)
                        return
                    
                    # Если нет конкретного обработчика, используем общий
                    if 'default_text' in self.handlers:
                        self.handlers['default_text'](self, update)
                        return
                
                # Если ничего не подошло
                self.send_message(chat_id, "❓ Не понимаю эту команду. Используйте кнопки меню.")
            
            # Обработка callback запросов
            elif 'callback_query' in update:
                callback_query = update['callback_query']
                chat_id = callback_query['message']['chat']['id']
                callback_data = callback_query['data']
                
                logger.info(f"Callback from {chat_id}: {callback_data}")
                
                # Отвечаем на callback query
                self.api.answer_callback_query(callback_query['id'])
                
                # Ищем обработчик
                for pattern, handler in self.handlers['callback'].items():
                    if callback_data.startswith(pattern):
                        handler(self, update)
                        return
                
                # Если нет обработчика
                self.send_message(chat_id, "❓ Неизвестная команда.")
                
        except Exception as e:
            logger.error(f"Error processing update: {e}")
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                self.send_message(chat_id, "Произошла ошибка. Попробуйте еще раз.")
    
    def send_message(self, chat_id: int, text: str, reply_markup: Dict = None, parse_mode: str = None):
        """Отправить сообщение"""
        try:
            return self.api.send_message(chat_id, text, reply_markup, parse_mode)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    def edit_message(self, chat_id: int, message_id: int, text: str, reply_markup: Dict = None):
        """Редактировать сообщение"""
        try:
            return self.api.edit_message_text(chat_id, message_id, text, reply_markup)
        except Exception as e:
            logger.error(f"Error editing message: {e}")
    
    def send_photo(self, chat_id: int, photo, caption: str = None, reply_markup: Dict = None):
        """Отправить фото"""
        try:
            return self.api.send_photo(chat_id, photo, caption, reply_markup)
        except Exception as e:
            logger.error(f"Error sending photo: {e}")
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """Скачать файл"""
        try:
            file_info = self.api.get_file(file_id)
            file_path = file_info['file_path']
            return self.api.download_file(file_path)
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            return None
    
    def start_polling(self, interval: float = 1.0):
        """Запустить polling"""
        logger.info("Starting bot polling...")
        
        try:
            # Проверяем бота
            bot_info = self.api.get_me()
            logger.info(f"Bot started: @{bot_info.get('username')} ({bot_info.get('first_name')})")
            
            # Удаляем webhook если установлен
            self.api.delete_webhook()
            
            self.running = True
            
            while self.running:
                try:
                    # Получаем обновления
                    updates = self.api.get_updates(
                        offset=self.last_update_id + 1,
                        limit=100,
                        timeout=10
                    )
                    
                    for update in updates:
                        self.last_update_id = update['update_id']
                        self.process_update(update)
                    
                    if not updates:
                        time.sleep(interval)
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.error(f"Polling error: {e}")
                    time.sleep(5)  # Ждем перед повторной попыткой
        
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            logger.info("Bot polling stopped")
    
    def stop_polling(self):
        """Остановить polling"""
        self.running = False

class MessageContext:
    """Контекст сообщения для удобства работы"""
    
    def __init__(self, bot: BotManager, update: Dict):
        self.bot = bot
        self.update = update
        
        if 'message' in update:
            self.message = update['message']
            self.chat_id = self.message['chat']['id']
            self.user = self.message['from']
            self.text = self.message.get('text', '')
        elif 'callback_query' in update:
            self.callback_query = update['callback_query']
            self.message = self.callback_query['message']
            self.chat_id = self.message['chat']['id']
            self.user = self.callback_query['from']
            self.callback_data = self.callback_query['data']
        
        self.user_state = bot.get_user_state(self.chat_id)
        self.user_data = bot.get_user_data(self.chat_id)
    
    def reply(self, text: str, reply_markup: Dict = None, parse_mode: str = None):
        """Ответить на сообщение"""
        return self.bot.send_message(self.chat_id, text, reply_markup, parse_mode)
    
    def edit_message(self, text: str, reply_markup: Dict = None):
        """Редактировать сообщение (для callback)"""
        if hasattr(self, 'callback_query'):
            return self.bot.edit_message(
                self.chat_id, 
                self.message['message_id'], 
                text, 
                reply_markup
            )
    
    def set_state(self, state: str):
        """Установить состояние пользователя"""
        self.bot.set_user_state(self.chat_id, state)
        self.user_state = state
    
    def set_data(self, key: str, value: Any):
        """Установить данные пользователя"""
        self.bot.set_user_data(self.chat_id, key, value)
        self.user_data[key] = value