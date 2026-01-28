from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from datetime import date

from .models import Booking
from .services import BookingService


class HomeView(View):
    """
    Главная страница с формой создания бронирования
    """

    def get(self, request):
        # Получаем последние 10 бронирований
        recent_bookings = Booking.objects.all()[:10]

        context = {
            'recent_bookings': recent_bookings,
            'today': date.today(),
        }
        return render(request, 'bookings/home.html', context)

    def post(self, request):
        """Обработка создания бронирования"""
        try:
            booking_data = {
                'user_email': request.POST.get('user_email'),
                'room_number': request.POST.get('room_number'),
                'booking_date': request.POST.get('booking_date'),
                'start_time': request.POST.get('start_time'),
                'end_time': request.POST.get('end_time'),
                'booking_type': request.POST.get('booking_type', 'lesson'),
                'purpose': request.POST.get('purpose', ''),
            }

            # Создаём бронирование через сервис
            booking_service = BookingService()
            booking, availability_result = booking_service.create_booking(booking_data)

            if booking.status == 'confirmed':
                messages.success(
                    request,
                    f'✅ Бронирование успешно подтверждено! Аудитория {booking.room_number} забронирована.'
                )
            else:
                messages.warning(
                    request,
                    f'❌ Бронирование отклонено: {availability_result.get("message", "Аудитория недоступна")}'
                )

            return redirect('booking_detail', pk=booking.pk)

        except Exception as e:
            messages.error(request, f'Ошибка при создании бронирования: {str(e)}')
            return redirect('home')


class BookingListView(ListView):
    """
    Список всех бронирований
    """
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 20

    def get_queryset(self):
        queryset = Booking.objects.all()

        # Фильтрация по email
        user_email = self.request.GET.get('email')
        if user_email:
            queryset = queryset.filter(user_email__icontains=user_email)

        # Фильтрация по статусу
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Фильтрация по дате
        booking_date = self.request.GET.get('date')
        if booking_date:
            queryset = queryset.filter(booking_date=booking_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_bookings'] = Booking.objects.count()
        context['confirmed_count'] = Booking.objects.filter(status='confirmed').count()
        context['rejected_count'] = Booking.objects.filter(status='rejected').count()
        return context


class BookingDetailView(DetailView):
    """
    Детальная информация о бронировании
    """
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'


class DeleteBookingView(View):
    """
    Удаление бронирования
    """

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        room_number = booking.room_number
        booking.delete()

        messages.success(
            request,
            f'Бронирование аудитории {room_number} успешно удалено'
        )
        return redirect('booking_list')