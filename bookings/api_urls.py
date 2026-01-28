from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import BookingViewSet, CreateBookingView, HealthCheckView

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('create-booking/', CreateBookingView.as_view(), name='api_create_booking'),
    path('health/', HealthCheckView.as_view(), name='api_health'),
]