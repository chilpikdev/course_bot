# bot/management/__init__.py
# Пустой файл

# bot/management/commands/__init__.py
# Пустой файл

# bot/management/commands/send_payment_notifications.py
"""
Django management команда для отправки уведомлений о платежах

Использование:
python manage.py send_payment_notifications
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from payments.models import Payment
from bot_manager import BotManager
from payment_handlers import send_payment_result_to_user
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send payment notifications to users'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--payment-id',
            type=int,
            help='Send notification for specific payment ID'
        )
        parser.add_argument(
            '--approved-only',
            action='store_true',
            help='Send notifications only for approved payments'
        )
        parser.add_argument(
            '--rejected-only', 
            action='store_true',
            help='Send notifications only for rejected payments'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending'
        )
    
    def handle(self, *args, **options):
        if not settings.TELEGRAM_BOT_TOKEN:
            self.stdout.write(
                self.style.ERROR('TELEGRAM_BOT_TOKEN not configured')
            )
            return
        
        try:
            bot = BotManager(settings.TELEGRAM_BOT_TOKEN)
            
            # Фильтруем платежи
            if options['payment_id']:
                payments = Payment.objects.filter(id=options['payment_id'])
            elif options['approved_only']:
                payments = Payment.objects.filter(
                    status='approved',
                    notification__user_notified_approved=False
                )
            elif options['rejected_only']:
                payments = Payment.objects.filter(
                    status='rejected', 
                    notification__user_notified_rejected=False
                )
            else:
                # Все неотправленные уведомления
                approved_payments = Payment.objects.filter(
                    status='approved',
                    notification__user_notified_approved=False
                )
                rejected_payments = Payment.objects.filter(
                    status='rejected',
                    notification__user_notified_rejected=False
                )
                payments = list(approved_payments) + list(rejected_payments)
            
            if not payments:
                self.stdout.write(
                    self.style.WARNING('No payments found to notify')
                )
                return
            
            self.stdout.write(f"Found {len(payments)} payments to notify")
            
            sent_count = 0
            error_count = 0
            
            for payment in payments:
                try:
                    approved = payment.status == 'approved'
                    
                    if options['dry_run']:
                        self.stdout.write(
                            f"Would send {('approval' if approved else 'rejection')} "
                            f"notification for payment {payment.id} to user {payment.user.chat_id}"
                        )
                    else:
                        send_payment_result_to_user(bot, payment, approved)
                        sent_count += 1
                        
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Sent {('approval' if approved else 'rejection')} "
                                f"notification for payment {payment.id}"
                            )
                        )
                
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error sending notification for payment {payment.id}: {e}"
                        )
                    )
            
            if not options['dry_run']:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully sent {sent_count} notifications"
                    )
                )
                if error_count > 0:
                    self.stdout.write(
                        self.style.WARNING(f"Failed to send {error_count} notifications")
                    )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Command failed: {e}")
            )
