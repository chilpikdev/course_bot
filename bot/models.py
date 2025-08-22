# bot/models.py

from django.db import models
from django.utils import timezone

class TelegramUser(models.Model):
    # BUL MODELDI ÓZGERTIW KEREK EMES. OL DURıS.
    chat_id = models.BigIntegerField(unique=True, verbose_name="Chat ID")
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Username")
    first_name = models.CharField(max_length=100, blank=True, verbose_name="Atı")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Familiyası")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    is_blocked = models.BooleanField(default=False, verbose_name="Bloklanǵan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dizimnen ótken sáne")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Jańalanǵan sáne")
    last_activity = models.DateTimeField(default=timezone.now, verbose_name="Sońǵı aktivlik")
    language = models.CharField(max_length=2, choices=[('qr', 'Qaraqalpaq'), ('uz', 'Uzbek')], null=True, blank=True)

    class Meta:
        verbose_name = "Telegram paydalanıwshısı"
        verbose_name_plural = "Telegram paydalanıwshıları"
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
        return " ".join(filter(None, parts)) or "Kórsetilmegen"

    def update_activity(self):
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])


class UserState(models.Model):
    # BUL MODELDI DE ÓZGERTIW KEREK EMES
    user = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, related_name='state', verbose_name="Paydalanıwshı")
    current_state = models.CharField(max_length=50, default='start', verbose_name="Házirgi jaǵdayı")
    state_data = models.JSONField(default=dict, blank=True, verbose_name="Jaǵday maǵlıwmatları")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Jańalandı")

    class Meta:
        verbose_name = "Paydalanıwshı jaǵdayı"
        verbose_name_plural = "Paydalanıwshılar jaǵdayları"

    def __str__(self):
        return f"{self.user} - {self.current_state}"


class InfoPage(models.Model):
    """Statik sahifalar (Biz haqimizda, Qo'llab-quvvatlash va h.k.)"""

    key = models.CharField(
        max_length=50, unique=True, verbose_name="Kilt sóz",
        help_text="Mısalı: about, support"
    )
    # 'content' qatarı ekige bólindi
    content_qr = models.TextField(verbose_name="Mazmunı (Qaraqalpaqsha)", help_text="HTML formatta jazıw múmkin")
    content_uz = models.TextField(verbose_name="Mazmuni (O'zbekcha)", help_text="HTML formatda yozish mumkin")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Informaciya beti"
        verbose_name_plural = "Informaciya betleri"

    def get_content(self, lang_code: str):
        return getattr(self, f'content_{lang_code}', self.content_qr)