# bot/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import TelegramUser, UserState, InfoPage


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = [
        'chat_id', 'username', 'full_name', 'phone', 
        'is_active', 'is_blocked', 'created_at', 'last_activity'
    ]
    list_filter = ['is_active', 'is_blocked', 'created_at', 'last_activity']
    search_fields = ['chat_id', 'username', 'first_name', 'last_name', 'phone']
    readonly_fields = ['chat_id', 'created_at', 'updated_at', 'last_activity']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('chat_id', 'username', 'first_name', 'last_name', 'phone')
        }),
        ('Статус', {
            'fields': ('is_active', 'is_blocked')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at', 'last_activity'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['activate_users', 'deactivate_users', 'block_users', 'unblock_users']
    
    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"Активировано {count} пользователей.")
    activate_users.short_description = "Активировать выбранных пользователей"
    
    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"Деактивировано {count} пользователей.")
    deactivate_users.short_description = "Деактивировать выбранных пользователей"
    
    def block_users(self, request, queryset):
        count = queryset.update(is_blocked=True)
        self.message_user(request, f"Заблокировано {count} пользователей.")
    block_users.short_description = "Заблокировать выбранных пользователей"
    
    def unblock_users(self, request, queryset):
        count = queryset.update(is_blocked=False)
        self.message_user(request, f"Разблокировано {count} пользователей.")
    unblock_users.short_description = "Разблокировать выбранных пользователей"


@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ("key", "updated_at")
    search_fields = ("key", "content_qr", "content_uz")
    
    fieldsets = (
        (None, {
            'fields': ('key',)
        }),
        ('Mazmunı (Qaraqalpaqsha)', {
            'fields': ('content_qr',)
        }),
        ('Mazmuni (O‘zbekcha)', {
            'fields': ('content_uz',)
        })
    )