import requests
from django.conf import settings
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class AvailabilityService:
    """
    Сервис для взаимодействия с API проверки доступности (Студент B)
    """

    def __init__(self):
        self.base_url = settings.AVAILABILITY_SERVICE_URL
        self.timeout = 10  # секунды

    def check_availability(self, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Отправляет запрос на проверку доступности аудитории

        Args:
            booking_data: Данные о бронировании

        Returns:
            Ответ от сервиса доступности
        """
        try:
            self.base_url = settings.AVAILABILITY_SERVICE_URL
            url = f"{self.base_url}/check-availability/"

            # Формируем данные для отправки
            payload = {
                'room_number': booking_data.get('room_number'),
                'booking_date': str(booking_data.get('booking_date')),
                'start_time': str(booking_data.get('start_time')),
                'end_time': str(booking_data.get('end_time')),
                'booking_type': booking_data.get('booking_type'),
            }

            logger.info(f"Отправка запроса на проверку доступности: {url}")
            logger.info(f"Данные: {payload}")

            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )

            response.raise_for_status()
            result = response.json()

            logger.info(f"Получен ответ от сервиса доступности: {result}")

            return {
                'success': True,
                'available': result.get('available', False),
                'message': result.get('message', ''),
                'conflicts': result.get('conflicts', []),
                'response_data': result
            }

        except requests.exceptions.Timeout:
            logger.error("Превышено время ожидания ответа от сервиса доступности")
            return {
                'success': False,
                'available': False,
                'message': 'Сервис проверки доступности не отвечает (timeout)',
                'error': 'timeout'
            }

        except requests.exceptions.ConnectionError:
            logger.error("Ошибка подключения к сервису доступности")
            return {
                'success': False,
                'available': False,
                'message': 'Не удалось подключиться к сервису проверки доступности',
                'error': 'connection_error'
            }

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP ошибка от сервиса доступности: {e}")
            try:
                error_data = e.response.json()
            except:
                error_data = {'detail': str(e)}

            return {
                'success': False,
                'available': False,
                'message': f'Ошибка сервиса доступности: {error_data.get("detail", str(e))}',
                'error': 'http_error',
                'response_data': error_data
            }

        except Exception as e:
            logger.error(f"Неожиданная ошибка при проверке доступности: {e}")
            return {
                'success': False,
                'available': False,
                'message': f'Произошла ошибка при проверке доступности: {str(e)}',
                'error': 'unexpected_error'
            }


class BookingService:
    """
    Бизнес-логика для работы с бронированиями
    """

    def __init__(self):
        self.availability_service = AvailabilityService()

    def create_booking(self, booking_data: Dict[str, Any]) -> tuple:
        """
        Создаёт бронирование с проверкой доступности

        Args:
            booking_data: Данные о бронировании

        Returns:
            tuple: (booking_object, availability_result)
        """
        from .models import Booking

        # Проверяем доступность через внешний сервис
        availability_result = self.availability_service.check_availability(booking_data)

        # Определяем статус на основе результата проверки
        if availability_result['success'] and availability_result['available']:
            status = 'confirmed'
        else:
            status = 'rejected'

        # Создаём запись о бронировании
        booking = Booking.objects.create(
            user_email=booking_data['user_email'],
            room_number=booking_data['room_number'],
            booking_date=booking_data['booking_date'],
            start_time=booking_data['start_time'],
            end_time=booking_data['end_time'],
            booking_type=booking_data.get('booking_type', 'lesson'),
            purpose=booking_data.get('purpose', ''),
            status=status,
            availability_check_response=availability_result
        )

        return booking, availability_result