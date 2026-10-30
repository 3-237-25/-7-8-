# Структура базы данных

## Основные модели

### Приложение Tickets
- **Category**: `id` (PK), `name` (Unique), `description`. Справочник категорий заявок.
- **Ticket**: 
  - `id` (PK)
  - `title` (Название заявки, мин. 5 символов)
  - `description` (Описание)
  - `category` (FK → Category, on_delete=PROTECT)
  - `owner` (FK → User, on_delete=CASCADE)
  - `status` (Выбор из: `new`, `progress`, `done`)
  - `created_at` (Дата и время создания)

### Приложение Bookings
- **Room**: `id` (PK), `name` (Unique), `capacity`, `is_available` (Boolean).
- **Booking**: 
  - `id` (PK)
  - `room` (FK → Room, on_delete=PROTECT)
  - `owner` (FK → User, on_delete=CASCADE)
  - `status` (Выбор из: `created`, `approved`, `completed`, `rejected`)
  - `purpose` (Цель бронирования, мин. 10 символов)
  - `created_at` (Дата и время создания)
- **BookingHistory**: 
  - `id` (PK)
  - `booking` (FK → Booking, on_delete=CASCADE)
  - `action` (Действие: Создана/Подтверждена/Завершена/Отклонена)
  - `timestamp` (Время события)
  - `user` (FK → User, on_delete=SET_NULL)

## Бизнес-правила на уровне БД и ORM
1. **Целостность ссылок**: Нельзя удалить категорию или комнату, если на них есть активные заявки или брони (используется `PROTECT`).
2. **Каскадное удаление**: При удалении пользователя его заявки и брони удаляются автоматически (`CASCADE`), но в истории бронирований остаётся запись с `user=NULL` (`SET_NULL`) для аудита.
3. **Уникальность**: Названия комнат и категорий должны быть уникальными.
4. **Валидация статусов заявок**: Переходы статусов контролируются на уровне сериализатора DRF (запрещено пропускать этап «В работе»).
5. **Валидация статусов бронирований**: Разрешены только переходы `created → approved/rejected` и `approved → completed`. Прямые переходы запрещены.
6. **Транзакционная целостность**: Подтверждение брони — составная операция, изменяющая статус брони и флаг доступности комнаты в одной транзакции (`@transaction.atomic`).