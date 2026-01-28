from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Booking
    """

    class Meta:
        model = Booking
        fields = [
            'id',
            'user_email',
            'room_number',
            'booking_date',
            'start_time',
            'end_time',
            'booking_type',
            'purpose',
            'status',
            'availability_check_response',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'status', 'availability_check_response', 'created_at', 'updated_at']


class BookingCreateSerializer(serializers.Serializer):
    """
    Сериализатор для создания бронирования
    """
    user_email = serializers.EmailField()
    room_number = serializers.CharField(max_length=50)
    booking_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    booking_type = serializers.ChoiceField(
        choices=['lesson', 'exam', 'meeting'],
        default='lesson'
    )
    purpose = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        """Проверка времени"""
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError(
                "Время начала должно быть раньше времени окончания"
            )
        return data