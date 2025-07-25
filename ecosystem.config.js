module.exports = {
  apps: [
    {
      name: "django_server",
      cwd: "./",
      interpreter: ".venv/bin/python",
      script: "-m",
      args: "uvicorn course_bot_project.asgi:application --host 0.0.0.0 --port 8000"
    },
    {
      name: "telegram_bot",
      cwd: "./",
      interpreter: ".venv/bin/python",
      script: "bot_polling.py"
    },
    {
      name: "celery_worker",
      cwd: "./",
      interpreter: ".venv/bin/python",
      script: "-m",
      args: "celery -A course_bot_project worker --loglevel=info"
    }
  ]
}
