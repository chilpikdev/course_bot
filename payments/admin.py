# payments/admin.py
# Расширенная админка для управления платежами

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import Payment, Advertisement, PaymentNotification, TelegramUser
# send message module
from bot.bot_manager import BotManager
from .tasks import send_advertisement_task

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user_info', 'course', 'amount', 'status_colored',
        'receipt_preview', 'created_at', 'quick_actions'
    ]
    list_filter = ['status', 'course', 'payment_method', 'created_at', 'approved_at']
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name', 'user__chat_id',
        'course__name_qr', 'course__name_uz', 'comment', 'user_comment'
    ]
    readonly_fields = ['created_at', 'updated_at', 'approved_at', 'file_info']
    
    fieldsets = (
        ('Информация о платеже', {
            'fields': ('user', 'course', 'amount', 'payment_method')
        }),
        ('Чек и комментарии', {
            'fields': ('receipt_file', 'file_info', 'user_comment')
        }),
        ('Статус и обработка', {
            'fields': ('status', 'comment', 'approved_by', 'link_sent')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at', 'approved_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['approve_payments', 'reject_payments', 'send_links']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve/<int:payment_id>/', self.admin_site.admin_view(self.approve_payment), name='approve_payment'),
            path('reject/<int:payment_id>/', self.admin_site.admin_view(self.reject_payment), name='reject_payment'),
            path('send_link/<int:payment_id>/', self.admin_site.admin_view(self.send_link), name='send_link'),
            path('send_notification/', self.admin_site.admin_view(self.send_test_notification), name='send_test_notification'),
        ]
        return custom_urls + urls
    
    def user_info(self, obj):
        user_link = reverse('admin:bot_telegramuser_change', args=[obj.user.pk])
        return format_html(
            '<a href="{}">{}</a><br>'
            '<small>@{} | ID: {}</small>',
            user_link,
            obj.user.full_name,
            obj.user.username or 'нет',
            obj.user.chat_id
        )
    user_info.short_description = "Пользователь"
    user_info.admin_order_field = 'user__first_name'
    
    def status_colored(self, obj):
        colors = {
            'pending': '#f39c12',    # оранжевый
            'approved': '#27ae60',   # зеленый
            'rejected': '#e74c3c',   # красный
            'cancelled': '#95a5a6'   # серый
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#000'),
            obj.get_status_display()
        )
    status_colored.short_description = "Статус"
    status_colored.admin_order_field = 'status'
    
    def receipt_preview(self, obj):
        if obj.receipt_file:
            if obj.is_image:
                return format_html(
                    '<a href="{}" target="_blank">'
                    '<img src="{}" style="max-width: 100px; max-height: 60px; border-radius: 4px;">'
                    '</a>',
                    obj.receipt_file.url,
                    obj.receipt_file.url
                )
            elif obj.is_pdf:
                return format_html(
                    '<a href="{}" target="_blank" style="text-decoration: none;">'
                    '<span style="color: #e74c3c;">📄 PDF</span>'
                    '</a>',
                    obj.receipt_file.url
                )
            else:
                return format_html(
                    '<a href="{}" target="_blank">📎 Файл</a>',
                    obj.receipt_file.url
                )
        return "Нет файла"
    receipt_preview.short_description = "Чек"
    
    def file_info(self, obj):
        if obj.receipt_file:
            try:
                size_mb = obj.receipt_file.size / (1024 * 1024)
                return format_html(
                    '<strong>Файл:</strong> {}<br>'
                    '<strong>Размер:</strong> {:.2f} МБ<br>'
                    '<strong>Тип:</strong> {}',
                    obj.receipt_file.name.split('/')[-1],
                    size_mb,
                    "Изображение" if obj.is_image else "PDF" if obj.is_pdf else "Документ"
                )
            except:
                return "Информация недоступна"
        return "Файл не загружен"
    file_info.short_description = "Информация о файле"
    
    def quick_actions(self, obj):
        if obj.status == 'pending':
            approve_url = reverse('admin:approve_payment', args=[obj.id])
            reject_url = reverse('admin:reject_payment', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" style="background: #27ae60; color: white;">✅ Одобрить</a><br>'
                '<a class="button" href="{}" style="background: #e74c3c; color: white; position: relative; bottom: -10px;">❌ Отклонить</a>',
                approve_url,
                reject_url
            )
        elif obj.status == 'approved' and not obj.link_sent:
            send_link_url = reverse('admin:send_link', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" style="background: #3498db; color: white;">🔗 Отправить ссылку</a>',
                send_link_url
            )
        elif obj.status == 'approved' and obj.link_sent:
            return format_html(
                '<span style="color: #27ae60;">✅ Ссылка отправлена</span>'
            )
        else:
            return ""
    quick_actions.short_description = "Действия"
    
    def approve_payment(self, request, payment_id):
        """Быстрое одобрение платежа"""
        payment = get_object_or_404(Payment, id=payment_id)
        
        if payment.status != 'pending':
            messages.error(request, f"Платеж уже обработан (статус: {payment.get_status_display()})")
        else:
            payment.approve(admin_user=request.user)
            messages.success(request, f"Платеж #{payment.id} одобрен")
            
            # Отправляем уведомление пользователю
            self.send_bot_notification(payment, approved=True)
        
        return redirect('admin:payments_payment_changelist')
    
    def reject_payment(self, request, payment_id):
        """Быстрое отклонение платежа"""
        payment = get_object_or_404(Payment, id=payment_id)
        
        if payment.status != 'pending':
            messages.error(request, f"Платеж уже обработан (статус: {payment.get_status_display()})")
        else:
            reason = request.GET.get('reason', 'Платеж не прошел проверку')
            payment.reject(comment=reason, admin_user=request.user)
            messages.success(request, f"Платеж #{payment.id} отклонен")
            
            # Отправляем уведомление пользователю
            self.send_bot_notification(payment, approved=False)
        
        return redirect('admin:payments_payment_changelist')
    
    def send_link(self, request, payment_id):
        """Отправить ссылку на группу"""
        payment = get_object_or_404(Payment, id=payment_id)
        
        if payment.status != 'approved':
            messages.error(request, "Можно отправлять ссылки только для одобренных платежей")
        else:
            # Отправляем ссылку
            self.send_bot_notification(payment, approved=True, force_send_link=True)
            payment.link_sent = True
            payment.save()
            messages.success(request, f"Ссылка отправлена пользователю {payment.user.full_name}")
        
        return redirect('admin:payments_payment_changelist')
    
    def send_bot_notification(self, payment, approved, force_send_link=False):
        """Отправить уведомление через бота"""
        try:
            from bot.bot_manager import BotManager
            from bot.payment_handlers import send_payment_result_to_user
            
            if not settings.TELEGRAM_BOT_TOKEN:
                return
            
            bot = BotManager(settings.TELEGRAM_BOT_TOKEN)
            
            if force_send_link or not (payment.notification.user_notified_approved if approved else payment.notification.user_notified_rejected):
                send_payment_result_to_user(bot, payment, approved)
                
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error sending bot notification: {e}")
    
    def send_test_notification(self, request):
        """Тестовое уведомление"""
        try:
            from bot.bot_manager import BotManager
            
            if not settings.TELEGRAM_BOT_TOKEN:
                return JsonResponse({"error": "Bot token not configured"})
            
            bot = BotManager(settings.TELEGRAM_BOT_TOKEN)
            
            # Отправляем тестовое сообщение админу
            admin_chat_id = getattr(settings, 'TELEGRAM_ADMIN_CHAT_ID', None)
            if admin_chat_id:
                bot.send_message(
                    admin_chat_id,
                    "🧪 Тестовое сообщение от Django админки!\n\n"
                    "Уведомления работают корректно."
                )
                return JsonResponse({"success": "Test notification sent"})
            else:
                return JsonResponse({"error": "Admin chat ID not configured"})
                
        except Exception as e:
            return JsonResponse({"error": str(e)})
    
    def approve_payments(self, request, queryset):
        """Массовое одобрение платежей"""
        count = 0
        for payment in queryset.filter(status='pending'):
            payment.approve(admin_user=request.user)
            self.send_bot_notification(payment, approved=True)
            count += 1
        
        self.message_user(request, f"Одобрено {count} платежей.")
    approve_payments.short_description = "✅ Одобрить выбранные платежи"
    
    def reject_payments(self, request, queryset):
        """Массовое отклонение платежей"""
        count = 0
        for payment in queryset.filter(status='pending'):
            payment.reject(admin_user=request.user)
            self.send_bot_notification(payment, approved=False)
            count += 1
        
        self.message_user(request, f"Отклонено {count} платежей.")
    reject_payments.short_description = "❌ Отклонить выбранные платежи"
    
    def send_links(self, request, queryset):
        """Массовая отправка ссылок"""
        count = 0
        for payment in queryset.filter(status='approved', link_sent=False):
            self.send_bot_notification(payment, approved=True, force_send_link=True)
            payment.link_sent = True
            payment.save()
            count += 1
        
        self.message_user(request, f"Отправлено {count} ссылок.")
    send_links.short_description = "🔗 Отправить ссылки на группы"

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'target_info', 'is_sent', 
        'success_count', 'failed_count', 'created_at', 'send_actions'
    ]
    list_filter = ['is_sent', 'target_all_users', 'target_active_only', 'created_at']
    search_fields = ['title', 'text']
    readonly_fields = ['sent_at', 'is_sent', 'success_count', 'failed_count', 'created_at']
    
    fieldsets = (
        ('Содержание', {
            'fields': ('title', 'text', 'image')
        }),
        ('Кнопка (необязательно)', {
            'fields': ('button_text', 'button_url'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['send_advertisements']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send/<int:ad_id>/', self.admin_site.admin_view(self.send_advertisement), name='send_advertisement'),
        ]
        return custom_urls + urls
    
    def target_info(self, obj):
        info = "Всем" if obj.target_all_users else "Выборочно"
        if obj.target_active_only:
            info += " (только активным)"
        return info
    target_info.short_description = "Целевая аудитория"
    
    def send_actions(self, obj):
        if not obj.is_sent:
            send_url = reverse('admin:send_advertisement', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" style="background: #3498db; color: white;">📤 Отправить</a>',
                send_url
            )
        else:
            return format_html(
                '<span style="color: #27ae60;">✅ Отправлено</span><br>'
                '<small>{}</small>',
                obj.sent_at.strftime('%d.%m.%Y %H:%M') if obj.sent_at else ''
            )
    send_actions.short_description = "Действия"
    
    def send_advertisement(self, request, ad_id):
        ad = get_object_or_404(Advertisement, id=ad_id)

        if ad.is_sent:
            messages.error(request, "Объявление уже отправлено")
        else:
            send_advertisement_task.delay(ad.id)  # Async fon rejimida ishlaydi
            messages.success(request, f"Объявление \"{ad.title}\" поставлено в очередь")
        ad.is_sent = True
        ad.save()
        
        return redirect('admin:payments_advertisement_changelist')
    
    def send_advertisements(self, request, queryset):
        """Массовая отправка объявлений"""
        count = queryset.filter(is_sent=False).count()
        
        for ad in queryset.filter(is_sent=False):
            ad.is_sent = True
            ad.sent_at = timezone.now()
            ad.success_count = 5  # Заглушка
            ad.save()
        
        self.message_user(request, f"Отправлено {count} объявлений.")
    send_advertisements.short_description = "📤 Отправить выбранные объявления"

