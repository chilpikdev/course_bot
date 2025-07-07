
# bot/management/commands/check_bot_status.py
"""
Django management команда для проверки статуса бота

Использование:
python manage.py check_bot_status
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from bot.bot_manager import BotManager
from bot.models import TelegramUser
from courses.models import Course
from payments.models import Payment

class Command(BaseCommand):
    help = 'Check bot status and statistics'
    
    def handle(self, *args, **options):
        self.stdout.write("🤖 Checking bot status...")
        
        # Проверка токена
        if not settings.TELEGRAM_BOT_TOKEN:
            self.stdout.write(
                self.style.ERROR('❌ TELEGRAM_BOT_TOKEN not configured')
            )
            return
        
        try:
            # Проверка подключения к Telegram
            bot = BotManager(settings.TELEGRAM_BOT_TOKEN)
            bot_info = bot.api.get_me()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Bot connected: @{bot_info.get('username')} ({bot_info.get('first_name')})"
                )
            )
            
            # Статистика базы данных
            total_users = TelegramUser.objects.count()
            active_users = TelegramUser.objects.filter(is_active=True).count()
            users_with_phone = TelegramUser.objects.exclude(phone__isnull=True).exclude(phone='').count()
            
            total_courses = Course.objects.count()
            active_courses = Course.objects.filter(is_active=True).count()
            
            total_payments = Payment.objects.count()
            pending_payments = Payment.objects.filter(status='pending').count()
            approved_payments = Payment.objects.filter(status='approved').count()
            
            self.stdout.write("\n📊 Statistics:")
            self.stdout.write(f"   Users: {total_users} total, {active_users} active, {users_with_phone} with phone")
            self.stdout.write(f"   Courses: {total_courses} total, {active_courses} active")
            self.stdout.write(f"   Payments: {total_payments} total, {pending_payments} pending, {approved_payments} approved")
            
            # Проверка настроек админа
            admin_chat_id = getattr(settings, 'TELEGRAM_ADMIN_CHAT_ID', None)
            if admin_chat_id:
                self.stdout.write(f"✅ Admin chat ID configured: {admin_chat_id}")
            else:
                self.stdout.write(
                    self.style.WARNING('⚠️  TELEGRAM_ADMIN_CHAT_ID not configured')
                )
            
            self.stdout.write(
                self.style.SUCCESS('\n🎉 Bot status check completed')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Bot connection failed: {e}')
            )
