# Система управления заявками (Tickets)

Django-приложение для управления заявками на обслуживание с полным REST API, серверной валидацией, разграничением доступа и историей изменений.


## Быстрый старт (Локальный запуск)

### Требования
- Python 3.8+
- Git

### Установка и запуск
1. Клонируйте репозиторий:
```bash
   git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
   cd <имя_папки_проекта>
```
2. Создайте и активируйте виртуальное окружение:
```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
```
3. Установите зависимости:
```bash
   pip install -r requirements.txt
```
4. Создайте файл .env на основе .env.example и заполните его (для локальной разработки можно оставить DJANGO_DEBUG=True и DATABASE_URL=sqlite:///db.sqlite3).
5. Примените миграции и создайте суперпользователя:
```bash
   python manage.py migrate
   python manage.py createsuperuser
```
6. Запустите сервер разработки:
```bash
   python manage.py runserver
```
Приложение доступно по адресу: http://127.0.0.1:8000/

## Функциональность
- **Система заявок (Tickets)**: CRUD операций, категории, фильтрация по статусу, поиск, строгие переходы статусов (Новая → В работе → Выполнена).
- **Система бронирования (Bookings)**: Бронирование переговорных комнат с проверкой доступности ресурса, история событий (создание/подтверждение/завершение/отклонение), транзакционные операции, 4 состояния.
- **Безопасность**: Разграничение доступа (пользователь видит и меняет только свои объекты), серверная валидация, CSRF-защита.
## Технологический стек
- **Backend**: Python, Django, Django REST Framework
- **Database**: PostgreSQL (production), SQLite (development)
- **Frontend**: HTML5, JavaScript (Fetch API), Tabler UI
- **Deployment**: Gunicorn, WhiteNoise, Render.com