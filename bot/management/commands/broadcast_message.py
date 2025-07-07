
# bot/management/commands/broadcast_message.py
"""
Django management команда для массовой рассылки

Использование:
python manage.py broadcast_message "Ваше сообщение" --active-only
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from bot.models import TelegramUser
from bot_manager import BotManager
import time

class Command(BaseCommand):
    help = 'Broadcast message to all users'
    
    def add_arguments(self, parser):
        parser.add_argument('message', type=str, help='Message to broadcast')
        parser.add_argument(
            '--active-only',
            action='store_true',
            help='Send only to active users'
        )
        parser.add_argument(
            '--with-phone-only',
            action='store_true',
            help='Send only to users with phone numbers'
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=0.1,
            help='Delay between messages in seconds (default: 0.1)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending'
        )
    
    def handle(self, *args, **options):
        message = options['message']
        
        if not settings.TELEGRAM_BOT_TOKEN:
            self.stdout.write(
                self.style.ERROR('TELEGRAM_BOT_TOKEN not configured')
            )
            return
        
        # Фильтруем пользователей
        users = TelegramUser.objects.all()
        
        if options['active_only']:
            users = users.filter(is_active=True)
        
        if options['with_phone_only']:
            users = users.exclude(phone__isnull=True).exclude(phone='')
        
        user_count = users.count()
        
        if user_count == 0:
            self.stdout.write(
                self.style.WARNING('No users found matching criteria')
            )
            return
        
        self.stdout.write(f"Found {user_count} users to send message to")
        
        if options['dry_run']:
            self.stdout.write("DRY RUN - Message would be:")
            self.stdout.write(f'"{message}"')
            self.stdout.write(f"Would be sent to {user_count} users")
            return
        
        # Подтверждение
        confirm = input(f"Send message to {user_count} users? (yes/no): ")
        if confirm.lower() != 'yes':
            self.stdout.write("Cancelled")
            return
        
        try:
            bot = BotManager(settings.TELEGRAM_BOT_TOKEN)
            
            sent_count = 0
            error_count = 0
            
            for user in users:
                try:
                    bot.send_message(user.chat_id, message)
                    sent_count += 1
                    
                    if sent_count % 10 == 0:
                        self.stdout.write(f"Sent {sent_count}/{user_count}")
                    
                    time.sleep(options['delay'])
                
                except Exception as e:
                    error_count += 1
                    if error_count <= 5:  # Показываем только первые 5 ошибок
                        self.stdout.write(
                            self.style.WARNING(f"Failed to send to {user.chat_id}: {e}")
                        )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"Broadcast completed: {sent_count} sent, {error_count} failed"
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Broadcast failed: {e}")
            )