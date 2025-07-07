# bot/views.py

import json
import logging
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from .bot_manager import BotManager
from .bot_handlers_simple import setup_bot_handlers

logger = logging.getLogger('bot')

# Глобальная переменная для хранения экземпляра бота
_bot_instance = None

def get_bot_instance():
    """Получить экземпляр бота (singleton)"""
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = BotManager(settings.TELEGRAM_BOT_TOKEN)
        setup_bot_handlers(_bot_instance)
        logger.info("Bot instance created and configured")
    return _bot_instance

@csrf_exempt
@require_POST
def webhook(request):
    """
    Обработчик webhook для Telegram бота
    """
    try:
        # Получаем данные от Telegram
        update_data = json.loads(request.body)
        logger.info(f"Webhook received update from user: {update_data.get('message', {}).get('from', {}).get('id', 'unknown')}")
        
        # Получаем экземпляр бота
        bot = get_bot_instance()
        
        # Обрабатываем обновление
        bot.process_update(update_data)
        
        return HttpResponse("OK")
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON in webhook request")
        return HttpResponse("Bad Request", status=400)
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return HttpResponse("Internal Server Error", status=500)

def set_webhook(request):
    """
    Установка webhook для бота
    """
    try:
        webhook_url = settings.TELEGRAM_WEBHOOK_URL
        
        if not webhook_url:
            return JsonResponse({
                "status": "error", 
                "message": "TELEGRAM_WEBHOOK_URL не настроен в settings"
            })
        
        # Получаем экземпляр бота
        bot = get_bot_instance()
        
        # Устанавливаем webhook
        result = bot.api.set_webhook(webhook_url)
        
        if result:
            logger.info(f"Webhook set successfully: {webhook_url}")
            return JsonResponse({
                "status": "success", 
                "message": "Webhook установлен успешно",
                "url": webhook_url
            })
        else:
            return JsonResponse({
                "status": "error", 
                "message": "Не удалось установить webhook"
            })
            
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return JsonResponse({
            "status": "error", 
            "message": f"Ошибка установки webhook: {str(e)}"
        })

def delete_webhook(request):
    """
    Удаление webhook (для переключения на polling)
    """
    try:
        # Получаем экземпляр бота
        bot = get_bot_instance()
        
        # Удаляем webhook
        result = bot.api.delete_webhook()
        
        if result:
            logger.info("Webhook deleted successfully")
            return JsonResponse({
                "status": "success", 
                "message": "Webhook удален успешно"
            })
        else:
            return JsonResponse({
                "status": "error", 
                "message": "Не удалось удалить webhook"
            })
            
    except Exception as e:
        logger.error(f"Error deleting webhook: {e}")
        return JsonResponse({
            "status": "error", 
            "message": f"Ошибка удаления webhook: {str(e)}"
        })

def bot_info(request):
    """
    Получение информации о боте
    """
    try:
        # Получаем экземпляр бота
        bot = get_bot_instance()
        
        # Получаем информацию о боте
        info = bot.api.get_me()
        
        return JsonResponse({
            "status": "success",
            "bot_info": {
                "id": info.get('id'),
                "username": info.get('username'),
                "first_name": info.get('first_name'),
                "is_bot": info.get('is_bot'),
                "can_join_groups": info.get('can_join_groups'),
                "can_read_all_group_messages": info.get('can_read_all_group_messages'),
                "supports_inline_queries": info.get('supports_inline_queries')
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting bot info: {e}")
        return JsonResponse({
            "status": "error",
            "message": f"Ошибка получения информации о боте: {str(e)}"
        })

def bot_status(request):
    """
    Статус бота и статистика
    """
    try:
        # Получаем экземпляр бота
        bot = get_bot_instance()
        
        # Проверяем подключение
        bot_info_data = bot.api.get_me()
        
        # Статистика пользователей
        from bot.models import TelegramUser
        total_users = TelegramUser.objects.count()
        active_users = TelegramUser.objects.filter(is_active=True).count()
        
        # Статистика курсов
        from courses.models import Course
        total_courses = Course.objects.count()
        active_courses = Course.objects.filter(is_active=True).count()
        
        return JsonResponse({
            "status": "success",
            "bot_online": True,
            "bot_username": bot_info_data.get('username'),
            "statistics": {
                "total_users": total_users,
                "active_users": active_users,
                "total_courses": total_courses,
                "active_courses": active_courses,
                "user_states_in_memory": len(bot.user_states),
                "user_data_in_memory": len(bot.user_data)
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting bot status: {e}")
        return JsonResponse({
            "status": "error",
            "bot_online": False,
            "message": f"Ошибка проверки статуса: {str(e)}"
        })