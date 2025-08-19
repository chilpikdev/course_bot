# Django + Telegram Bot + Celery: Запуск проекта

---

## Чтобы запустить проект **Django + Telegram Bot + Celery**, делай так:

### 1. Клонируй репозиторий:

   ```bash
   git clone https://github.com/chilpikdev/course_bot.git
   cd course_bot
   ```

### 2. Установи зависимости для Python:

   ```bash
   sudo apt install python3.10-venv -y

   python -m venv .venv
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

### 3. Подними Django:

   ```bash
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   ```

### 4. Поставь Node.js и PM2:

   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

   export NVM_DIR="$HOME/.nvm"
   [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
   [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

   nvm install --lts
   npm install -g pm2
   ```

### 5. Запусти процессы через PM2:

   ```bash
   pm2 start .venv/bin/python --name django_server -- \
     -m uvicorn course_bot_project.asgi:application --host 0.0.0.0 --port 8000

   pm2 start .venv/bin/python --name telegram_bot -- bot_polling.py

   pm2 start .venv/bin/python --name celery_worker -- \
     -m celery -A course_bot_project worker --loglevel=info
   ```

### 6. Настрой автозапуск:

   ```bash
   pm2 startup
   pm2 save
   ```

---

## Управлять можно так:

* `pm2 logs` — все логи
* `pm2 logs django_server` — логи Django
* `pm2 logs telegram_bot` — логи бота
* `pm2 logs celery_worker` — логи Celery
* `pm2 stop all` — остановить все процессы
* `pm2 restart all` — перезапустить
* `pm2 delete all` — удалить

---

## Важно:

* После обновления проекта не забудь сделать `pm2 restart all` и `pm2 save`, иначе после перезагрузки сервера ничего не поднимется.
* Redis должен быть запущен (`redis-server`).

