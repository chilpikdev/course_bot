# Django + Telegram Bot + Celery: Запуск проекта

## ⬇️ 1. Клонирование проекта

```bash
git clone https://github.com/chilpikdev/course_bot.git
cd course_bot
```

## 🐍 2. Создание виртуального окружения

```bash
python -m venv .venv
source .venv/bin/activate
```

## 📥 3. Установка необходимых библиотек

```bash
pip install -r requirements.txt
```

## ⚙️ 4. Выполнение миграций и создание суперпользователя

```bash
python manage.py migrate
python manage.py createsuperuser
```

## 🚀 5. Запуск всех сервисов через PM2

```bash
pm2 start process.json
```

## 📄 6. Просмотр логов

```bash
pm2 logs          # все логи
pm2 logs django_server
pm2 logs telegram_bot
pm2 logs celery_worker
```

## 🛑 7. Остановка или удаление сервисов

```bash
pm2 stop all
pm2 restart all
pm2 delete all
```


---

## ⚙️ 8. Автоматический запуск при перезагрузке сервера (Linux)

```bash
pm2 startup
```

Команда отобразит нужную команду `systemctl`, которую необходимо скопировать и вставить в терминал.

После этого выполните команду **`pm2 save`**:

```bash
pm2 save
```

---

### 🔁 Полная последовательность запуска

```bash
pm2 start process.json
pm2 save
pm2 startup     # выполняется один раз
```

---

### 📌 Важно

* Если вы обновили проект и выполнили `pm2 restart`, но забыли выполнить `pm2 save`, то после перезагрузки сервера ничего не запустится автоматически.

* Redis-сервер должен быть запущен:

  ```bash
  redis-server
  ```
