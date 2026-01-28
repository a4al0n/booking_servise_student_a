import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class AvailabilityService:
    """
    Сервис для взаимодействия с API проверки доступности
    """

    def __init__(self):
        self.base_url = settings.AVAILABILITY_SERVICE_URL
        self.timeout = 10

    def check_availability(self, booking_data):
        """
        Проверка доступности аудитории
        """
        # ИСПРАВЛЕНО: убрано дублирование пути
        url = f"{self.base_url}/check-availability/"

        payload = {
            'room_number': booking_data.get('room_number'),
            'booking_date': str(booking_data.get('booking_date')),
            'start_time': str(booking_data.get('start_time')),
            'end_time': str(booking_data.get('end_time')),
            'booking_type': booking_data.get('booking_type'),
        }

        try:
            logger.info(f"Отправка запроса в сервис доступности: {url}")
            logger.debug(f"Payload: {payload}")

            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )

            logger.info(f"Получен ответ: статус {response.status_code}")

            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                logger.warning(f"Ошибка от сервиса доступности: {response.text}")
                return {
                    'success': False,
                    'error': f"Ошибка сервиса доступности (код {response.status_code})",
                    'details': response.text
                }

        except requests.exceptions.Timeout:
            logger.error("Превышено время ожидания")
            return {
                'success': False,
                'error': 'Превышено время ожидания'
            }

        except requests.exceptions.ConnectionError:
            logger.error("Не удалось подключиться")
            return {
                'success': False,
                'error': 'Не удалось подключиться к сервису доступности'
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе: {str(e)}")
            return {
                'success': False,
                'error': f'Ошибка при запросе: {str(e)}'
            }