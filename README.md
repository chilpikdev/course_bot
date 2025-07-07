## Быстрый старт

1. Клонируйте репозиторий и установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

2. Проведите миграции:
    ```sh
    python manage.py migrate
    ```

3. Создайте суперпользователя для доступа к админке:
    ```sh
    python manage.py createsuperuser
    ```

4. Запустите сервер Django:
    ```sh
    python manage.py runserver
    ```

5. Запустите Telegram-бота:
    Чтобы настроить вебхук, откройте http://example.com/bot/set_webhook/

6. Откройте админку по адресу http://example.com/admin/ и настройте курсы, способы оплаты и пользователей.