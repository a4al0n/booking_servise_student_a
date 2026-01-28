from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer
from .services import BookingService


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с бронированиями

    Endpoints:
    - GET /api/bookings/ - список всех бронирований
    - GET /api/bookings/{id}/ - детали бронирования
    - POST /api/bookings/ - создание бронирования (не используется, см. CreateBookingView)
    - DELETE /api/bookings/{id}/ - удаление бронирования
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        """Фильтрация по email пользователя, если указан"""
        queryset = Booking.objects.all()
        user_email = self.request.query_params.get('user_email', None)

        if user_email:
            queryset = queryset.filter(user_email=user_email)

        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Статистика бронирований
        GET /api/bookings/stats/
        """
        total = Booking.objects.count()
        confirmed = Booking.objects.filter(status='confirmed').count()
        rejected = Booking.objects.filter(status='rejected').count()
        pending = Booking.objects.filter(status='pending').count()

        return Response({
            'total': total,
            'confirmed': confirmed,
            'rejected': rejected,
            'pending': pending
        })


class CreateBookingView(APIView):
    """
    API для создания бронирования с проверкой доступности

    POST /api/create-booking/

    Request body:
    {
        "user_email": "user@example.com",
        "room_number": "101",
        "booking_date": "2026-02-15",
        "start_time": "10:00",
        "end_time": "12:00",
        "booking_type": "lesson",
        "purpose": "Лекция по программированию"
    }

    Response:
    {
        "success": true,
        "message": "Бронирование успешно создано",
        "booking": {...},
        "availability_check": {...}
    }
    """

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Ошибка валидации данных',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        booking_data = serializer.validated_data
        booking_service = BookingService()

        try:
            booking, availability_result = booking_service.create_booking(booking_data)

            return Response({
                'success': True,
                'message': self._get_success_message(booking, availability_result),
                'booking': BookingSerializer(booking).data,
                'availability_check': availability_result
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Ошибка при создании бронирования: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _get_success_message(self, booking, availability_result):
        """Формирует сообщение на основе результата проверки"""
        if booking.status == 'confirmed':
            return 'Бронирование успешно подтверждено!'
        else:
            return f'Бронирование отклонено: {availability_result.get("message", "Аудитория недоступна")}'


class HealthCheckView(APIView):
    """
    Проверка работоспособности сервиса
    GET /api/health/
    """

    def get(self, request):
        return Response({
            'status': 'ok',
            'service': 'booking-service',
            'version': '1.0.0'
        })