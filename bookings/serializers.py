from rest_framework import serializers
from .models import Room, Booking, BookingHistory


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "name", "capacity", "is_available")


class BookingHistorySerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = BookingHistory
        fields = ("id", "action", "timestamp", "user_username")


class BookingSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source="room.name", read_only=True)
    history = BookingHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ("id", "room", "room_name", "owner", "status", "purpose", "created_at", "history")
        read_only_fields = ("id", "owner", "created_at", "history")

    def validate_purpose(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Цель бронирования должна содержать не менее 10 символов.")
        return value.strip()

    def validate(self, attrs):
        if self.instance:
            old_status = self.instance.status
            new_status = attrs.get("status", old_status)

            allowed_transitions = {
                "created": {"approved", "rejected"},
                "approved": {"completed"},
                "completed": set(),
                "rejected": set(),
            }

            if new_status != old_status and new_status not in allowed_transitions.get(old_status, set()):
                raise serializers.ValidationError(
                    {"status": f"Недопустимый переход из '{old_status}' в '{new_status}'."})
        return attrs