# Архитектура приложения

## Общая схема взаимодействия
```text
[Браузер пользователя (Tabler UI + JS Fetch)] 
       │ (HTTPS/HTTP + JSON + CSRF Token)
       ▼
[Облачный веб-сервис (Render) / Локальный сервер]
       │ (WSGI через Gunicorn)
       ▼
[Django + Django REST Framework]
       │ (Django ORM + dj-database-url)
       ▼
[PostgreSQL (Постоянное хранение)]
       
[WhiteNoise Middleware] → Обслуживание собранных статических файлов (CSS/JS)
```

## Компоненты системы
1. Frontend: HTML-шаблоны (templates/), клиентская логика на Vanilla JS (static/), библиотека Tabler UI для стилизации.
2. Backend:
   - `tickets`: управление заявками (модели `Category`, `Ticket`).
   - `bookings`: бронирование ресурсов (модели `Room`, `Booking`, `BookingHistory`).
   - `accounts`: управление пользователями и аутентификация.
   - `config`: глобальные настройки, маршрутизация, WSGI-конфигурация.
3. REST API: Django REST Framework с аутентификацией через сессии (SessionAuthentication) и проверкой прав (IsAuthenticated).
4. База данных: PostgreSQL для промышленной эксплуатации. Используются ограничения целостности (PROTECT, CASCADE).

## Безопасность
- Защита от CSRF-атак для всех изменяющих запросов (POST, PATCH, DELETE).
- Фильтрация QuerySet на уровне представлений: owner=self.request.user.
- Конфиденциальные данные (SECRET_KEY, пароли БД) вынесены в переменные окружения.
- В режиме эксплуатации DEBUG=False, подробные трейсбеки не показываются пользователю.