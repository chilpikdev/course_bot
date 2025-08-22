# courses/models.py

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Course(models.Model):
    """Модель курса"""
    
    name_qr = models.CharField(max_length=200, verbose_name="Название (Каракалпакский)")
    name_uz = models.CharField(max_length=200, verbose_name="Название (Узбекский)")
    
    description_qr = models.TextField(verbose_name="Описание (Каракалпакский)")
    description_uz = models.TextField(verbose_name="Описание (Узбекский)")
    
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Цена", help_text="Цена курса в сумах"
    )
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, 
        validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Старая цена"
    )
    group_link = models.URLField(verbose_name="Ссылка на группу")
    preview_image = models.ImageField(upload_to='courses/images/', blank=True, null=True, verbose_name="Изображение курса")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    max_students = models.PositiveIntegerField(blank=True, null=True, verbose_name="Максимум студентов")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['order', 'name_qr']

    def __str__(self):
        return self.name_qr

    def get_name(self, lang_code: str):
        return getattr(self, f'name_{lang_code}', self.name_qr)

    def get_description(self, lang_code: str):
        return getattr(self, f'description_{lang_code}', self.description_qr)

    @property
    def current_students_count(self):
        # Bu funkciya iskerligine tásir etpeydi, ózgerissiz qaladı
        return self.payments.filter(status='approved').count()

    @property
    def is_available(self):
        # Bu funkciya iskerligine tásir etpeydi, ózgerissiz qaladı
        if not self.is_active: return False
        if self.max_students and self.current_students_count >= self.max_students: return False
        return True

    @property
    def discount_percentage(self):
        # Bu funkciya iskerligine tásir etpeydi, ózgerissiz qaladı
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

class PaymentMethod(models.Model):
    """Модель способа оплаты"""
    
    name_qr = models.CharField(max_length=100, verbose_name="Название (Каракалпакский)")
    name_uz = models.CharField(max_length=100, verbose_name="Название (Узбекский)")
    
    card_number = models.CharField(max_length=20, blank=True, verbose_name="Номер карты")
    cardholder_name = models.CharField(max_length=200, blank=True, verbose_name="Получатель")
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="Название банка")
    
    instructions_qr = models.TextField(blank=True, verbose_name="Инструкция (Каракалпакский)")
    instructions_uz = models.TextField(blank=True, verbose_name="Инструкция (Узбекский)")

    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"
        ordering = ['order', 'name_qr']

    def __str__(self):
        return self.name_qr

    def get_name(self, lang_code: str):
        return getattr(self, f'name_{lang_code}', self.name_qr)
        
    def get_instructions(self, lang_code: str):
        return getattr(self, f'instructions_{lang_code}', self.instructions_qr)