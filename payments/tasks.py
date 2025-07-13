# your_app/tasks.py
from celery import shared_task
from .models import Advertisement, TelegramUser
from django.conf import settings
from bot.bot_manager import BotManager
from django.utils import timezone

@shared_task
def send_advertisement_task(ad_id):
    ad = Advertisement.objects.get(id=ad_id)
    # if ad.is_sent:
    #     return

    users = TelegramUser.objects.filter(is_active=True)
    bot = BotManager(settings.TELEGRAM_BOT_TOKEN)

    reply_markup = None
    if ad.button_text:
        reply_markup = {
            'inline_keyboard': [[{
                'text': ad.button_text,
                'url': ad.button_url
            }]]
        }

    n = 0
    k = 0

    for user in users:
        try:
            if ad.image:
                bot.send_photo(
                    chat_id=user.chat_id,
                    photo=f'{settings.BASE_URL}{ad.image.url}',
                    caption=ad.text,
                    reply_markup=reply_markup
                )
            else:
                bot.send_message(
                    chat_id=user.chat_id,
                    text=ad.text,
                    reply_markup=reply_markup
                )
            n += 1
        except:
            k += 1

    ad.is_sent = True
    ad.sent_at = timezone.now()
    ad.success_count = n
    ad.failed_count = k
    ad.save()
