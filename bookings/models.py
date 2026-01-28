from django.db import models
from django.core.exceptions import ValidationError


class Booking(models.Model):
    """
    Модель бронирования аудитории
    """
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('confirmed', 'Подтверждено'),
        ('rejected', 'Отклонено'),
    ]

    BOOKING_TYPE_CHOICES = [
        ('lesson', 'Занятие'),
        ('exam', 'Экзамен'),
        ('meeting', 'Собрание'),
    ]

    # Информация о пользователе
    user_email = models.EmailField(verbose_name='Email пользователя')

    # Информация о бронировании
    room_number = models.CharField(max_length=50, verbose_name='Номер аудитории')
    booking_date = models.DateField(verbose_name='Дата бронирования')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')
    booking_type = models.CharField(
        max_length=20,
        choices=BOOKING_TYPE_CHOICES,
        default='lesson',
        verbose_name='Тип бронирования'
    )
    purpose = models.TextField(verbose_name='Цель бронирования', blank=True)

    # Статус и результат проверки
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    availability_check_response = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Ответ от сервиса доступности'
    )

    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.room_number} - {self.booking_date} ({self.user_email})"

    def clean(self):
        """Валидация данных"""
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError('Время начала должно быть раньше времени окончания')
