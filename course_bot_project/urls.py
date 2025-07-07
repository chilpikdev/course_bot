# course_bot_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from decouple import config

# Получаем URL админки из настроек
admin_url = config('ADMIN_URL', default='admin/')

urlpatterns = [
    path(admin_url, admin.site.urls),
    path('bot/', include('bot.urls')),
    path('payments/', include('payments.urls')),
    path('courses/', include('courses.urls')),
]

# Обслуживание медиа файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Настройка админки
admin.site.site_header = "Управление курсами и ботом"
admin.site.site_title = "Course Bot Admin"
admin.site.index_title = "Панель управления"