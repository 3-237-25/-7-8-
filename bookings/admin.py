from django.contrib import admin
from .models import Room, Booking, BookingHistory

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "capacity", "is_available")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "owner", "status", "created_at")
    list_filter = ("status", "room")

@admin.register(BookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ("booking", "action", "user", "timestamp")
    list_filter = ("action",)