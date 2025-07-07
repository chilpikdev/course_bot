# telegram_api.py
# Простой клиент для работы с Telegram Bot API через HTTP

import requests
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class TelegramAPI:
    """Простой клиент для Telegram Bot API"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.session = requests.Session()
        self.session.timeout = 30
    
    def _make_request(self, method: str, params: Dict = None, files: Dict = None) -> Dict:
        """Выполнить HTTP запрос к Telegram API"""
        url = f"{self.base_url}/{method}"
        print(params)
        
        try:
            if files:
                # Для загрузки файлов используем multipart/form-data
                response = self.session.post(url, data=params, files=files)
            else:
                # Для обычных запросов используем JSON
                response = self.session.post(url, json=params)
            
            response.raise_for_status()
            result = response.json()
            
            if not result.get('ok'):
                error_msg = result.get('description', 'Unknown error')
                logger.error(f"Telegram API error: {error_msg}")
                raise Exception(f"Telegram API error: {error_msg}")
            
            return result.get('result')
            
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request error: {e}")
            raise Exception(f"HTTP request error: {e}")
        except Exception as e:
            logger.error(f"Telegram API request failed: {e}")
            raise
    
    def get_me(self) -> Dict:
        """Получить информацию о боте"""
        return self._make_request('getMe')
    
    def get_updates(self, offset: int = None, limit: int = 100, timeout: int = 0) -> List[Dict]:
        """Получить обновления (для polling)"""
        params = {
            'limit': limit,
            'timeout': timeout
        }
        if offset:
            params['offset'] = offset
            
        return self._make_request('getUpdates', params)
    
    def set_webhook(self, url: str) -> bool:
        """Установить webhook"""
        params = {'url': url}
        result = self._make_request('setWebhook', params)
        return result is True
    
    def delete_webhook(self) -> bool:
        """Удалить webhook"""
        result = self._make_request('deleteWebhook')
        return result is True
    
    def send_message(self, chat_id: int, text: str, reply_markup: Dict = None, 
                    parse_mode: str = None) -> Dict:
        """Отправить текстовое сообщение"""
        params = {
            'chat_id': chat_id,
            'text': text
        }
        
        if reply_markup:
            params['reply_markup'] = json.dumps(reply_markup)
        
        if parse_mode:
            params['parse_mode'] = parse_mode
            
        return self._make_request('sendMessage', params)
    
    def send_photo(self, chat_id: int, photo, caption: str = None, 
                  reply_markup: Dict = None) -> Dict:
        """Отправить фото"""
        params = {
            'chat_id': chat_id
        }
        
        if caption:
            params['caption'] = caption
            
        if reply_markup:
            params['reply_markup'] = json.dumps(reply_markup)
        
        files = None
        if isinstance(photo, str):
            # Если это URL или file_id
            params['photo'] = photo
        else:
            # Если это файл
            files = {'photo': photo}
            
        return self._make_request('sendPhoto', params, files)
    
    def send_document(self, chat_id: int, document, caption: str = None) -> Dict:
        """Отправить документ"""
        params = {
            'chat_id': chat_id
        }
        
        if caption:
            params['caption'] = caption
        
        files = None
        if isinstance(document, str):
            # Если это URL или file_id
            params['document'] = document
        else:
            # Если это файл
            files = {'document': document}
            
        return self._make_request('sendDocument', params, files)
    
    def edit_message_text(self, chat_id: int, message_id: int, text: str, 
                         reply_markup: Dict = None, parse_mode: str = None) -> Dict:
        """Редактировать текст сообщения"""
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text
        }
        
        if reply_markup:
            params['reply_markup'] = json.dumps(reply_markup)
            
        if parse_mode:
            params['parse_mode'] = parse_mode
            
        return self._make_request('editMessageText', params)
    
    def delete_message(self, chat_id: int, message_id: int) -> bool:
        """Удалить сообщение"""
        params = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        
        result = self._make_request('deleteMessage', params)
        return result is True
    
    def answer_callback_query(self, callback_query_id: str, text: str = None, 
                             show_alert: bool = False) -> bool:
        """Ответить на callback query"""
        params = {
            'callback_query_id': callback_query_id
        }
        
        if text:
            params['text'] = text
            
        if show_alert:
            params['show_alert'] = show_alert
            
        result = self._make_request('answerCallbackQuery', params)
        return result is True
    
    def get_file(self, file_id: str) -> Dict:
        """Получить информацию о файле"""
        params = {'file_id': file_id}
        return self._make_request('getFile', params)
    
    def download_file(self, file_path: str) -> bytes:
        """Скачать файл"""
        url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"File download error: {e}")
            raise Exception(f"File download error: {e}")

class KeyboardBuilder:
    """Помощник для создания клавиатур"""
    
    @staticmethod
    def reply_keyboard(buttons: List[List[str]], resize_keyboard: bool = True, 
                      one_time_keyboard: bool = False) -> Dict:
        """Создать обычную клавиатуру"""
        keyboard = []
        for row in buttons:
            keyboard_row = []
            for button in row:
                if button == "📱 Поделиться номером":
                    # Специальная кнопка для запроса контакта
                    keyboard_row.append({
                        'text': button,
                        'request_contact': True
                    })
                else:
                    keyboard_row.append({'text': button})
            keyboard.append(keyboard_row)
        
        return {
            'keyboard': keyboard,
            'resize_keyboard': resize_keyboard,
            'one_time_keyboard': one_time_keyboard
        }
    
    @staticmethod
    def inline_keyboard(buttons: List[List[Dict]]) -> Dict:
        """Создать inline клавиатуру"""
        keyboard = []
        for row in buttons:
            keyboard_row = []
            for button in row:
                keyboard_row.append({
                    'text': button['text'],
                    'callback_data': button['callback_data']
                })
            keyboard.append(keyboard_row)
        
        return {
            'inline_keyboard': keyboard
        }
    
    @staticmethod
    def remove_keyboard() -> Dict:
        """Удалить клавиатуру"""
        return {'remove_keyboard': True}