import subprocess
import time
import sys

def run_command(command, description):
    """Выполняет системную команду с отображением статуса."""
    print(f"{description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Успешно: {description}\n")
    except subprocess.CalledProcessError:
        print(f"Ошибка при выполнении: {description}")
        print("Проверьте, запущен ли Docker и свободны ли порты.")
        sys.exit(1)

def main():
    # Создание .env файла
    print("\n===  АВТОМАТИЧЕСКАЯ НАСТРОЙКА ПРОЕКТА  ===\n")
    print("Этот скрипт поможет развернуть приложение через Docker Compose,")
    print("создать конфигурационный файл и подготовить базу данных.\n")

    print("Шаг 1: Конфигурация окружения (.env)")
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write("DEBUG=True\n")
            f.write("SECRET_KEY=secret-key-auto-generated\n")
            f.write("ALLOWED_HOSTS=*\n")
            f.write("DATABASE_URL=postgres://postgres:postgres@db:5432/failover_db\n")
            f.write("CELERY_BROKER_URL=redis://redis:6379/0\n")
            f.write("CELERY_RESULT_BACKEND=redis://redis:6379/0\n")
        print("Файл .env успешно создан/обновлен.\n")
    except Exception as e:
        print(f"Ошибка при создании .env: {e}")
        sys.exit(1)

    # Сборка контейнеров
    print("Шаг 2: Сборка и запуск контейнеров")
    run_command("docker compose build --no-cache", "Сборка Docker-образов (без кэша)")
    run_command("docker compose up -d", "Запуск сервисов в фоновом режиме")
    
    # Ожидание БД
    print("Ожидание инициализации базы данных (10 секунд)...")
    time.sleep(10)

    # Миграции
    print("Шаг 3: Настройка базы данных")
    run_command("docker compose exec web python manage.py migrate", "Применение миграций Django")

    # Создание суперюзера (опционально)
    print("Шаг 4: Учетная запись администратора")
    create_admin = input("Хотите создать суперюзера (admin) сейчас? [y/N]: ").strip().lower()
    
    if create_admin == 'y':
        username = input("Имя пользователя (по умолчанию: admin): ").strip() or "admin"
        email = input("Email (по умолчанию: admin@example.com): ").strip() or "admin@example.com"
        password = input("Пароль (по умолчанию: 1): ").strip() or "1"
        
        # Используем non-interactive режим создания пользователя через shell
        # Это предотвращает ошибки ввода внутри контейнера
        cmd = (
            f'docker compose exec web python manage.py shell -c '
            f'"from django.contrib.auth import get_user_model; '
            f'User = get_user_model(); '
            f'User.objects.create_superuser(\'{username}\', \'{email}\', \'{password}\') '
            f'if not User.objects.filter(username=\'{username}\').exists() '
            f'else print(\'Пользователь с таким именем уже существует\')"'
        )
        
        run_command(cmd, "Регистрация администратора")
        print(f"Данные для входа: Логин: {username} / Пароль: {password}")
    else:
        print("ℹСоздание администратора пропущено.")
    
    # Создание тестовых данных
    print("Шаг 5: Создание тестовых данных")
    # Создаем получателя с ID=1, у которого нет Телеграма (чтобы сработал Failover)
    seed_cmd = (
        f'docker compose exec web python manage.py shell -c '
        f'"from notifications.models import Recipient; '
        f'obj, created = Recipient.objects.get_or_create(pk=1, defaults={{'
        f'\'username\': \'TestUser\', '
        f'\'email\': \'test@example.com\', '
        f'\'phone\': \'+79991234567\', '
        f'\'telegram_id\': \'\'}}'  # Пустой ID, чтобы спровоцировать ошибку отправки в ТГ
        f'); '
        f'print(\'Создан тестовый получатель: TestUser (ID: 1)\' if created else \'Тестовый получатель уже существует\')"'
    )
    run_command(seed_cmd, "Генерация тестового пользователя")

    # Финал
    print("\n === УСТАНОВКА УСПЕШНО ЗАВЕРШЕНА === ")
    print("-" * 50)
    print(" API Endpoint:      http://localhost:8000/api/send/")
    print(" Админ-панель:      http://localhost:8000/admin/")
    print(" Логи приложения:   docker compose logs -f web")
    print(" Логи Celery:       docker compose logs -f worker")
    print("-" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Установка прервана пользователем.")
        sys.exit(0)