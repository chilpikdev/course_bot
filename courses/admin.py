# ===== courses/admin.py =====

from django.contrib import admin
from django.utils.html import format_html
from .models import Course, PaymentMethod

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'price', 'old_price', 'discount_info', 
        'current_students_count', 'is_active', 'is_featured', 'created_at'
    ]
    list_filter = ['is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'current_students_count']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'short_description', 'preview_image')
        }),
        ('Цены', {
            'fields': ('price', 'old_price')
        }),
        ('Настройки доступа', {
            'fields': ('group_link', 'max_students', 'is_active', 'is_featured', 'order')
        }),
        ('Статистика', {
            'fields': ('current_students_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['activate_courses', 'deactivate_courses', 'feature_courses']
    
    def discount_info(self, obj):
        if obj.discount_percentage > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">-{}%</span>',
                obj.discount_percentage
            )
        return "Нет скидки"
    discount_info.short_description = "Скидка"
    
    def activate_courses(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"Активировано {count} курсов.")
    activate_courses.short_description = "Активировать выбранные курсы"
    
    def deactivate_courses(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"Деактивировано {count} курсов.")
    deactivate_courses.short_description = "Деактивировать выбранные курсы"
    
    def feature_courses(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f"{count} курсов отмечены как рекомендуемые.")
    feature_courses.short_description = "Отметить как рекомендуемые"

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'card_number', 'cardholder_name', 'bank_name', 'is_active', 'order']
    list_filter = ['is_active', 'bank_name']
    search_fields = ['name', 'card_number', 'cardholder_name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'bank_name', 'is_active', 'order')
        }),
        ('Реквизиты', {
            'fields': ('card_number', 'cardholder_name')
        }),
        ('Инструкции', {
            'fields': ('instructions',)
        })
    )