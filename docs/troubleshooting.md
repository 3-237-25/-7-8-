# Диагностика типовых ошибок

### 1. Ошибка: `DisallowedHost at /`
- **Причина**: Домен, по которому обращаются к сайту, не указан в `ALLOWED_HOSTS`.
- **Решение**: Проверьте переменную окружения `DJANGO_ALLOWED_HOSTS`. Убедитесь, что там указан домен Render без `https://` и без пробелов (например, `myapp.onrender.com`).

### 2. Ошибка: `OperationalError: connection to server failed`
- **Причина**: Неверный `DATABASE_URL` или Web Service и PostgreSQL находятся в разных регионах.
- **Решение**: Убедитесь, что в переменной `DATABASE_URL` вставлен именно **Internal Database URL**, и что оба сервиса созданы в регионе `Oregon`.

### 3. Ошибка: `ProgrammingError: relation "tickets_ticket" does not exist`
- **Причина**: Миграции не были применены к облачной базе данных PostgreSQL.
- **Решение**: Откройте **Shell** в панели Render и выполните `python manage.py migrate`.

### 4. Проблема: Страница открывается без стилей (CSS/JS не загружаются, ошибка 404)
- **Причина**: Статические файлы не собраны или не отдаются сервером.
- **Решение**: Убедитесь, что в `settings.py` подключен `whitenoise.middleware.WhiteNoiseMiddleware`, задан `STATIC_ROOT`, и в `build.sh` присутствует команда `python manage.py collectstatic --noinput`.

### 5. Ошибка: `403 Forbidden` или `CSRF verification failed` при POST/PATCH запросах
- **Причина**: Отсутствует или не совпадает CSRF-токен, либо домен не добавлен в доверенные источники.
- **Решение**: Проверьте, что в JavaScript-запросе передаётся заголовок `X-CSRFToken`, а переменная `DJANGO_CSRF_TRUSTED_ORIGINS` содержит полный HTTPS-адрес вашего приложения.