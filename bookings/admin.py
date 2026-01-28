from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'room_number',
        'booking_date',
        'start_time',
        'end_time',
        'user_email',
        'booking_type',
        'status',
        'created_at'
    ]
    list_filter = ['status', 'booking_type', 'booking_date', 'created_at']
    search_fields = ['user_email', 'room_number', 'purpose']
    readonly_fields = ['created_at', 'updated_at', 'availability_check_response']

    fieldsets = (
        ('Информация о пользователе', {
            'fields': ('user_email',)
        }),
        ('Детали бронирования', {
            'fields': ('room_number', 'booking_date', 'start_time', 'end_time', 'booking_type', 'purpose')
        }),
        ('Статус', {
            'fields': ('status', 'availability_check_response')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )