from django.urls import path
from .views import (
    HomeView,
    BookingListView,
    BookingDetailView,
    DeleteBookingView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/<int:pk>/delete/', DeleteBookingView.as_view(), name='booking_delete'),
]