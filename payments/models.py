# payments/models.py

import os
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from bot.models import TelegramUser
from courses.models import Course, PaymentMethod

def receipt_upload_path(instance, filename):
    """Путь для загрузки чеков"""
    ext = filename.split('.')[-1]
    filename = f"receipt_{instance.user.chat_id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('receipts', str(instance.user.chat_id), filename)

class Payment(models.Model):
    """Модель платежа"""
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает проверки'),
        ('approved', 'Подтвержден'),
        ('rejected', 'Отклонен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Пользователь"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Курс"
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Способ оплаты"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Сумма оплаты"
    )
    receipt_file = models.FileField(
        upload_to=receipt_upload_path,
        verbose_name="Файл чека",
        help_text="Скриншот или PDF чека об оплате"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус платежа"
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий",
        help_text="Комментарий администратора"
    )
    user_comment = models.TextField(
        blank=True,
        verbose_name="Комментарий пользователя",
        help_text="Комментарий от пользователя при отправке чека"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    approved_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата подтверждения"
    )
    approved_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Подтвержден администратором"
    )
    link_sent = models.BooleanField(
        default=False,
        verbose_name="Ссылка отправлена",
        help_text="Была ли отправлена ссылка на группу пользователю"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ['-created_at']
        # unique_together = ['user', 'course', 'status']  # Один пользователь может купить курс только один раз

    def __str__(self):
        return f"{self.user} - {self.course.name} ({self.get_status_display()})"

    def approve(self, admin_user=None):
        """Подтвердить платеж"""
        self.status = 'approved'
        self.approved_at = timezone.now()
        if admin_user:
            self.approved_by = admin_user
        self.save()

    def reject(self, comment="", admin_user=None):
        """Отклонить платеж"""
        self.status = 'rejected'
        if comment:
            self.comment = comment
        if admin_user:
            self.approved_by = admin_user
        self.save()

    @property
    def file_extension(self):
        """Расширение файла чека"""
        if self.receipt_file:
            return os.path.splitext(self.receipt_file.name)[1].lower()
        return ""

    @property
    def is_image(self):
        """Является ли файл изображением"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        return self.file_extension in image_extensions

    @property
    def is_pdf(self):
        """Является ли файл PDF"""
        return self.file_extension == '.pdf'

class Advertisement(models.Model):
    """Модель рекламного объявления для массовой рассылки"""
    
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок"
    )
    text = models.TextField(
        verbose_name="Текст сообщения",
        help_text="Текст рекламного сообщения для отправки пользователям"
    )
    image = models.ImageField(
        upload_to='ads/',
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Изображение для прикрепления к сообщению"
    )
    button_text = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Текст кнопки",
        help_text="Текст для inline кнопки (необязательно)"
    )
    button_url = models.URLField(
        blank=True,
        verbose_name="Ссылка кнопки",
        help_text="URL для inline кнопки (необязательно)"
    )
    target_all_users = models.BooleanField(
        default=True,
        verbose_name="Отправить всем пользователям"
    )
    target_active_only = models.BooleanField(
        default=True,
        verbose_name="Только активным пользователям",
        help_text="Отправлять только пользователям, которые не заблокировали бота"
    )
    scheduled_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Запланированное время отправки",
        help_text="Оставьте пустым для немедленной отправки"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    sent_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Дата отправки"
    )
    is_sent = models.BooleanField(
        default=False,
        verbose_name="Отправлено"
    )
    success_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Успешно отправлено"
    )
    failed_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Не удалось отправить"
    )

    class Meta:
        verbose_name = "Рекламное объявление"
        verbose_name_plural = "Рекламные объявления"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def total_sent(self):
        """Общее количество отправленных сообщений"""
        return self.success_count + self.failed_count
    
    @property
    def image_url(self):
        """URL изображения, если есть"""
        if self.image:
            return self.image.url
        return None

class PaymentNotification(models.Model):
    """Модель для отслеживания уведомлений о платежах"""
    
    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        related_name='notification',
        verbose_name="Платеж"
    )
    admin_notified = models.BooleanField(
        default=False,
        verbose_name="Админ уведомлен"
    )
    user_notified_approved = models.BooleanField(
        default=False,
        verbose_name="Пользователь уведомлен об одобрении"
    )
    user_notified_rejected = models.BooleanField(
        default=False,
        verbose_name="Пользователь уведомлен об отклонении"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Уведомление о платеже"
        verbose_name_plural = "Уведомления о платежах"

    def __str__(self):
        return f"Уведомления для {self.payment}"