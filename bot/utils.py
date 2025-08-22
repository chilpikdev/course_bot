# bot/utils.py
# Ulıwma járdemshi funkciyalar ushın

from .models import TelegramUser

def get_user_language(chat_id: int) -> str:
    """Paydalanıwshınıń til kodın bazadan alıw"""
    try:
        user = TelegramUser.objects.get(chat_id=chat_id)
        # Eger paydalanıwshı til tańlamaǵan bolsa, standart til 'qr' boladı
        return user.language or 'qr'
    except TelegramUser.DoesNotExist:
        # Eger paydalanıwshı bazada joq bolsa (bul jaǵday kem ushırasadı), standart til qaytarıladı
        return 'qr'