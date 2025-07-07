# fix_bot_issue.py
# Скрипт для полного исправления проблем с python-telegram-bot

import os
import sys
import subprocess
import importlib

def run_command(command):
    """Выполнить команду и вернуть результат"""
    try:
        print(f"   Выполняется: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_and_remove_cached_modules():
    """Удалить кешированные модули"""
    print("🧹 Очистка кешированных модулей...")
    
    # Удаляем __pycache__ директории
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                import shutil
                shutil.rmtree(pycache_path)
                print(f"   Удален: {pycache_path}")
            except:
                pass
    
    # Удаляем .pyc файлы
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file))
                    print(f"   Удален: {file}")
                except:
                    pass

def main():
    print("🛠️  ПОЛНОЕ ИСПРАВЛЕНИЕ python-telegram-bot")
    print("=" * 50)
    
    # 1. Очистка кеша
    check_and_remove_cached_modules()
    
    # 2. Показываем текущую версию
    print("\n📦 Проверка текущих версий...")
    success, stdout, stderr = run_command("pip list | grep -i telegram")
    if stdout:
        print("   Текущие telegram пакеты:")
        print(f"   {stdout.strip()}")
    
    # 3. Полное удаление всех telegram пакетов
    print("\n🗑️  Удаление всех telegram пакетов...")
    telegram_packages = [
        "python-telegram-bot",
        "telegram", 
        "python-telegram-bot-raw",
        "PTB"
    ]
    
    for package in telegram_packages:
        success, stdout, stderr = run_command(f"pip uninstall {package} -y")
        if "Successfully uninstalled" in stdout:
            print(f"   ✅ {package} удален")
        elif "not installed" in stderr:
            print(f"   ℹ️  {package} не был установлен")
        else:
            print(f"   ⚠️  {package}: {stderr.strip()}")
    
    # 4. Очистка pip кеша
    print("\n🧽 Очистка pip кеша...")
    run_command("pip cache purge")
    
    # 5. Установка правильной версии
    print("\n📥 Установка python-telegram-bot 20.8...")
    success, stdout, stderr = run_command("pip install python-telegram-bot==20.8 --no-cache-dir")
    if success:
        print("   ✅ python-telegram-bot 20.8 установлен")
    else:
        print(f"   ❌ Ошибка установки: {stderr}")
        print("\n🔄 Попробуем альтернативный способ...")
        
        # Альтернативная установка
        success, stdout, stderr = run_command("pip install --force-reinstall --no-deps python-telegram-bot==20.8")
        if success:
            print("   ✅ Принудительная установка успешна")
        else:
            print(f"   ❌ Не удалось установить: {stderr}")
            return False
    
    # 6. Установка остальных зависимостей
    print("\n📦 Установка дополнительных зависимостей...")
    dependencies = [
        "asgiref==3.7.2",
        "pytz==2023.3",
        "httpx>=0.24.0",  # Для python-telegram-bot
        "certifi"
    ]
    
    for dep in dependencies:
        success, stdout, stderr = run_command(f"pip install {dep}")
        if success:
            print(f"   ✅ {dep} установлен")
        else:
            print(f"   ⚠️  {dep}: {stderr.strip()}")
    
    # 7. Проверка финальной установки
    print("\n🔍 Проверка установки...")
    success, stdout, stderr = run_command("pip list | grep -i telegram")
    if success and "python-telegram-bot" in stdout:
        print("   ✅ python-telegram-bot успешно установлен:")
        print(f"   {stdout.strip()}")
    else:
        print("   ❌ Проблема с финальной установкой")
        return False
    
    # 8. Тест импорта
    print("\n🧪 Тестирование импорта...")
    try:
        import telegram
        print(f"   ✅ telegram модуль: версия {telegram.__version__}")
        
        from telegram.ext import Application
        print("   ✅ Application импортирован")
        
        from telegram import Bot
        print("   ✅ Bot импортирован")
        
    except ImportError as e:
        print(f"   ❌ Ошибка импорта: {e}")
        return False
    
    # 9. Очистка кеша еще раз
    print("\n🧹 Финальная очистка...")
    check_and_remove_cached_modules()
    
    print("\n🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
    print("\n📋 Что делать дальше:")
    print("1. python simple_bot_test.py  # Простой тест")
    print("2. python check_config.py     # Полная проверка")
    print("3. python run_bot.py          # Запуск бота")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        if not success:
            print("\n❌ Исправление не удалось")
            print("Попробуйте создать новое виртуальное окружение:")
            print("python -m venv venv_new")
            print("source venv_new/bin/activate")
            print("pip install -r requirements.txt")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Прервано пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)