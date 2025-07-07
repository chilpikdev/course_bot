# bot/urls.py
from django.urls import path
from . import views

app_name = 'bot'

urlpatterns = [
    path('webhook/', views.webhook, name='webhook'),
    path('set_webhook/', views.set_webhook, name='set_webhook'),
    path('delete_webhook/', views.delete_webhook, name='delete_webhook'),
    path('info/', views.bot_info, name='bot_info'),
    path('status/', views.bot_status, name='bot_status'),
]