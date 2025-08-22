# bot/models.py

from django.db import models
from django.utils import timezone

class TelegramUser(models.Model):
    chat_id = models.BigIntegerField(unique=True, verbose_name="Chat ID")
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Username")
    first_name = models.CharField(max_length=100, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    last_activity = models.DateTimeField(default=timezone.now, verbose_name="Последняя активность")
    language = models.CharField(
        max_length=2, choices=[('qr', 'Qaraqalpaq'), ('uz', 'Uzbek')], 
        null=True, blank=True, verbose_name="Язык"
    )

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"
        ordering = ['-created_at']

    def __str__(self):
        if self.first_name:
            return f"{self.first_name} ({self.chat_id})"
        elif self.username:
            return f"@{self.username} ({self.chat_id})"
        return f"User {self.chat_id}"

    @property
    def full_name(self):
        parts = [self.first_name, self.last_name]
        return " ".join(filter(None, parts)) or "Не указано"

    def update_activity(self):
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])


class UserState(models.Model):
    user = models.OneToOneField(
        TelegramUser, on_delete=models.CASCADE, 
        related_name='state', verbose_name="Пользователь"
    )
    current_state = models.CharField(
        max_length=50, default='start', verbose_name="Текущее состояние"
    )
    state_data = models.JSONField(
        default=dict, blank=True, verbose_name="Данные состояния"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Состояние пользователя"
        verbose_name_plural = "Состояния пользователей"

    def __str__(self):
        return f"{self.user} - {self.current_state}"


class InfoPage(models.Model):
    """Модель для статических страниц (О нас, Поддержка и т.д.)"""

    key = models.CharField(
        max_length=50, unique=True, verbose_name="Ключ",
        help_text="Например: about, support"
    )
    content_qr = models.TextField(
        verbose_name="Содержимое (Каракалпакский)", 
        help_text="Можно использовать HTML-теги"
    )
    content_uz = models.TextField(
        verbose_name="Содержимое (Узбекский)", 
        help_text="Можно использовать HTML-теги"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Информационная страница"
        verbose_name_plural = "Информационные страницы"

    def get_content(self, lang_code: str):
        return getattr(self, f'content_{lang_code}', self.content_qr)