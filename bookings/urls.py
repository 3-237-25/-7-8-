from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import dashboard, RoomViewSet, BookingViewSet

router = DefaultRouter()
router.register("rooms", RoomViewSet, basename="rooms")
router.register("bookings", BookingViewSet, basename="bookings")

urlpatterns = [
    path("", dashboard, name="booking_dashboard"),
    path("api/", include(router.urls)),
]