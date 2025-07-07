# bot/models.py

from django.db import models
from django.utils import timezone

class TelegramUser(models.Model):
    """Модель пользователей Telegram бота"""
    
    chat_id = models.BigIntegerField(
        unique=True, 
        verbose_name="Chat ID",
        help_text="Уникальный идентификатор чата в Telegram"
    )
    username = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Username",
        help_text="Имя пользователя в Telegram (@username)"
    )
    first_name = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Фамилия"
    )
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name="Телефон",
        help_text="Номер телефона пользователя"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Может ли пользователь получать сообщения"
    )
    is_blocked = models.BooleanField(
        default=False,
        verbose_name="Заблокирован",
        help_text="Заблокирован ли пользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    last_activity = models.DateTimeField(
        default=timezone.now,
        verbose_name="Последняя активность"
    )

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"
        ordering = ['-created_at']

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.chat_id})"
        elif self.first_name:
            return f"{self.first_name} ({self.chat_id})"
        elif self.username:
            return f"@{self.username} ({self.chat_id})"
        return f"User {self.chat_id}"

    @property
    def full_name(self):
        """Полное имя пользователя"""
        parts = [self.first_name, self.last_name]
        return " ".join(filter(None, parts)) or "Не указано"

    def update_activity(self):
        """Обновить время последней активности"""
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])

class UserState(models.Model):
    """Модель для хранения состояния пользователя в боте"""
    
    user = models.OneToOneField(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='state',
        verbose_name="Пользователь"
    )
    current_state = models.CharField(
        max_length=50,
        default='start',
        verbose_name="Текущее состояние",
        help_text="Текущее состояние пользователя в диалоге с ботом"
    )
    state_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Данные состояния",
        help_text="Дополнительные данные для текущего состояния"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлено"
    )

    class Meta:
        verbose_name = "Состояние пользователя"
        verbose_name_plural = "Состояния пользователей"

    def __str__(self):
        return f"{self.user} - {self.current_state}"