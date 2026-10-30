from django.db import models
from django.conf import settings

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название комнаты")
    capacity = models.IntegerField(verbose_name="Вместимость (чел.)")
    is_available = models.BooleanField(default=True, verbose_name="Доступна для бронирования")

    def __str__(self):
        return self.name

class Booking(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "Создана"
        APPROVED = "approved", "Подтверждена"
        COMPLETED = "completed", "Завершена"
        REJECTED = "rejected", "Отклонена"

    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="bookings", verbose_name="Комната")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings", verbose_name="Владелец")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED, verbose_name="Статус")
    purpose = models.CharField(max_length=200, verbose_name="Цель бронирования")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Бронь: {self.room.name} ({self.owner.username})"

class BookingHistory(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="history", verbose_name="Бронирование")
    action = models.CharField(max_length=50, verbose_name="Действие")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время события")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Инициатор")

    def __str__(self):
        return f"{self.booking.id} - {self.action} ({self.timestamp})"