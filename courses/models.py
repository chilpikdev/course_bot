# courses/models.py

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Course(models.Model):
    """Модель курса"""
    
    name = models.CharField(
        max_length=200,
        verbose_name="Название курса"
    )
    description = models.TextField(
        verbose_name="Описание курса",
        help_text="Подробное описание курса для пользователей"
    )
    short_description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Краткое описание",
        help_text="Краткое описание для отображения в списке"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Цена",
        help_text="Цена курса в рублях"
    )
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Старая цена",
        help_text="Старая цена для показа скидки"
    )
    group_link = models.URLField(
        verbose_name="Ссылка на группу",
        help_text="Пригласительная ссылка в Telegram группу/канал"
    )
    preview_image = models.ImageField(
        upload_to='courses/images/',
        blank=True,
        null=True,
        verbose_name="Изображение курса"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Доступен ли курс для покупки"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Рекомендуемый",
        help_text="Показывать ли курс в рекомендуемых"
    )
    max_students = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Максимум студентов",
        help_text="Максимальное количество студентов (оставьте пустым для неограниченного)"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def current_students_count(self):
        """Количество текущих студентов"""
        return self.payments.filter(status='approved').count()

    @property
    def is_available(self):
        """Доступен ли курс для покупки"""
        if not self.is_active:
            return False
        if self.max_students and self.current_students_count >= self.max_students:
            return False
        return True

    @property
    def discount_percentage(self):
        """Процент скидки если есть старая цена"""
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    def get_display_description(self):
        """Получить описание для отображения"""
        return self.short_description if self.short_description else self.description[:300] + "..." if len(self.description) > 300 else self.description

class PaymentMethod(models.Model):
    """Модель способа оплаты"""
    
    name = models.CharField(
        max_length=100,
        verbose_name="Название способа оплаты"
    )
    card_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Номер карты"
    )
    cardholder_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Получатель",
        help_text="ФИО владельца карты"
    )
    bank_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Название банка"
    )
    instructions = models.TextField(
        blank=True,
        verbose_name="Инструкции по оплате"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_payment_info(self):
        """Получить информацию о способе оплаты для отправки пользователю"""
        info = f"💳 {self.name}\n"
        if self.card_number:
            info += f"Номер карты: {self.card_number}\n"
        if self.cardholder_name:
            info += f"Получатель: {self.cardholder_name}\n"
        if self.bank_name:
            info += f"Банк: {self.bank_name}\n"
        if self.instructions:
            info += f"\nИнструкции:\n{self.instructions}"
        return info