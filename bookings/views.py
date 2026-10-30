from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Room, Booking, BookingHistory
from .serializers import RoomSerializer, BookingSerializer
from rest_framework import serializers


@login_required(login_url="/admin/login/")
@ensure_csrf_cookie
def dashboard(request):
    return render(request, "bookings/dashboard.html")


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(owner=self.request.user).select_related('room').prefetch_related(
            'history').order_by('-created_at')

    def perform_create(self, serializer):
        with transaction.atomic():
            booking = serializer.save(owner=self.request.user)
            BookingHistory.objects.create(booking=booking, action="Создана", user=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        booking = self.get_object()
        if booking.status != "created":
            return Response({"error": "Можно подтвердить только бронь со статусом 'Создана'"}, status=400)

        with transaction.atomic():
            booking.status = "approved"
            booking.save()

            room = booking.room
            if not room.is_available:
                raise serializers.ValidationError("Комната уже занята!")
            room.is_available = False
            room.save()

            BookingHistory.objects.create(booking=booking, action="Подтверждена", user=request.user)

        return Response({"status": booking.status, "message": "Бронирование подтверждено"})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        booking = self.get_object()
        if booking.status != "approved":
            return Response({"error": "Можно завершить только подтверждённую бронь"}, status=400)

        with transaction.atomic():
            booking.status = "completed"
            booking.save()

            room = booking.room
            room.is_available = True
            room.save()

            BookingHistory.objects.create(booking=booking, action="Завершена", user=request.user)

        return Response({"status": booking.status, "message": "Бронирование завершено"})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        booking = self.get_object()
        if booking.status != "created":
            return Response({"error": "Можно отклонить только бронь со статусом 'Создана'"}, status=400)

        with transaction.atomic():
            booking.status = "rejected"
            booking.save()
            BookingHistory.objects.create(booking=booking, action="Отклонена", user=request.user)

        return Response({"status": booking.status, "message": "Бронирование отклонено"})
