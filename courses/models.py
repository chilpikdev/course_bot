# courses/models.py

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Course(models.Model):
    """Модель курса"""
    
    # 'name' hám 'description' qatarları ekige bólindi
    name_qr = models.CharField(max_length=200, verbose_name="Atı (Qaraqalpaqsha)")
    name_uz = models.CharField(max_length=200, verbose_name="Nomi (O'zbekcha)")
    
    description_qr = models.TextField(verbose_name="Sıpatlaması (Qaraqalpaqsha)")
    description_uz = models.TextField(verbose_name="Tavsifi (O'zbekcha)")
    
    # Qalǵan qatarlar tilge baylanıslı emes, ózgerissiz qaladı
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Bahası", help_text="Kurs bahası (sumda)"
    )
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, 
        validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Eski bahası"
    )
    group_link = models.URLField(verbose_name="Gruppaǵa silteme")
    preview_image = models.ImageField(upload_to='courses/images/', blank=True, null=True, verbose_name="Kurs súwreti")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    is_featured = models.BooleanField(default=False, verbose_name="Usınıs etilgen")
    max_students = models.PositiveIntegerField(blank=True, null=True, verbose_name="Maks. student sanı")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralaw tártibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Jaratılǵan sáne")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Jańalanǵan sáne")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['order', 'name_qr'] # Standart sıralaw ushın birinshi tildi paydalanamız

    def __str__(self):
        # Admin panelde qaraqalpaqsha atı kórinsin
        return self.name_qr

    # Bot kodın ańsatlastırıw ushın járdemshi funkciyalar
    def get_name(self, lang_code: str):
        return getattr(self, f'name_{lang_code}', self.name_qr)

    def get_description(self, lang_code: str):
        return getattr(self, f'description_{lang_code}', self.description_qr)

    @property
    def current_students_count(self):
        return self.payments.filter(status='approved').count()

    @property
    def is_available(self):
        if not self.is_active: return False
        if self.max_students and self.current_students_count >= self.max_students: return False
        return True

    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    # ESKI get_display_description() funkciyasın alıp tasladıq, sebebi endi get_description(lang_code) bar

class PaymentMethod(models.Model):
    """Модель способа оплаты"""
    
    # 'name' hám 'instructions' qatarları ekige bólindi
    name_qr = models.CharField(max_length=100, verbose_name="Atı (Qaraqalpaqsha)")
    name_uz = models.CharField(max_length=100, verbose_name="Nomi (O'zbekcha)")
    
    card_number = models.CharField(max_length=20, blank=True, verbose_name="Karta nomeri")
    cardholder_name = models.CharField(max_length=200, blank=True, verbose_name="Qabıllawshı")
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="Bank atı")
    
    instructions_qr = models.TextField(blank=True, verbose_name="Instrukciya (Qaraqalpaqsha)")
    instructions_uz = models.TextField(blank=True, verbose_name="Instruksiya (O'zbekcha)")

    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıralaw tártibi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Jaratılǵan sáne")

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

    # get_payment_info funkciyasın ALıP TASLAŃ!
    # Sebebi: Bul funkciya ishinde tekstler ("Karta nomeri:", "Qabıllawshı:") qattı kodlanǵan.
    # Bunday logikanı bot_handlers faylında translations.py arqalı qılıw durıs boladı.
    # Model tek maǵlıwmatlardı saqlawı kerek, kórsetiw logikasın emes.