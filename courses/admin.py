# ===== courses/admin.py =====

from django.contrib import admin
from django.utils.html import format_html
from .models import Course, PaymentMethod

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'name_qr', 'price', 'old_price', 'discount_info', 
        'current_students_count', 'is_active', 'is_featured'
    ]
    list_filter = ['is_active', 'is_featured', 'created_at']
    search_fields = ['name_qr', 'name_uz', 'description_qr', 'description_uz']
    readonly_fields = ['created_at', 'updated_at', 'current_students_count']
    
    fieldsets = (
        ('Kurs haqqında maǵlıwmat (Qaraqalpaqsha)', {
            'fields': ('name_qr', 'description_qr')
        }),
        ('Kurs haqida ma‘lumot (O‘zbekcha)', {
            'fields': ('name_uz', 'description_uz')
        }),
        ('Ulıwma maǵlıwmatlar', {
            'fields': ('preview_image', 'price', 'old_price', 'group_link', 'max_students')
        }),
        ('Sazlawlar', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Statistika (avtomatikalıq)', {
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
    list_display = ['name_qr', 'card_number', 'cardholder_name', 'is_active', 'order']
    list_filter = ['is_active', 'bank_name']
    search_fields = ['name_qr', 'name_uz', 'card_number', 'cardholder_name']
    
    fieldsets = (
        ('Tiykarǵı maǵlıwmatlar', {
            'fields': ('is_active', 'order', 'bank_name')
        }),
        ('Ataması (kóp tilli)', {
            'fields': ('name_qr', 'name_uz')
        }),
        ('Rekvizitler', {
            'fields': ('card_number', 'cardholder_name')
        }),
        ('Instrukciya (kóp tilli)', {
            'fields': ('instructions_qr', 'instructions_uz',)
        })
    )