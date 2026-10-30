# Инструкция по развёртыванию на Render.com

## 1. Подготовка базы данных PostgreSQL
1. В панели Render нажмите **New** → **PostgreSQL**.
2. Заполните параметры: Name (например, `pz8-django-db`), Region (`Oregon`), Plan (`Free`).
3. После создания (статус `Available`) перейдите в раздел **Connections** и скопируйте **Internal Database URL**.

## 2. Создание Web Service
1. Нажмите **New** → **Web Service** и подключите свой GitHub-репозиторий.
2. Заполните параметры:
   - **Name**: `pz8-django-app`
   - **Region**: Тот же, что и у БД (`Oregon`).
   - **Branch**: `main`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
   - **Plan**: `Free`

## 3. Настройка переменных окружения (Environment Variables)
Добавьте следующие переменные в настройках Web Service:
| KEY | VALUE |
|---|---|
| `DATABASE_URL` | *Вставьте Internal Database URL из шага 1* |
| `DJANGO_SECRET_KEY` | *Сгенерируйте случайную строку (мин. 50 символов)* |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `имя-вашего-приложения.onrender.com` (без https://) |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://имя-вашего-приложения.onrender.com` |

## 4. Запуск и миграции
1. Нажмите **Create Web Service**. Render автоматически выполнит `build.sh`.
2. После успешного запуска откройте вкладку **Shell** в панели управления сервисом.
3. Выполните команду для создания таблиц в облачной БД:
   ```bash
   python manage.py migrate
   ```
4. Создайте суперпользователя для входа в админ-панель:
   ```bash
   python manage.py createsuperuser
   ```