"""
Тестовый скрипт для проверки API
Запуск: python test_api.py
"""

import requests
import json
from datetime import date, timedelta

# URL вашего сервиса
BASE_URL = "http://localhost:8000/api"


def test_health_check():
    """Проверка работоспособности сервиса"""
    print("\n🔍 Тест 1: Health Check")
    print("-" * 50)

    response = requests.get(f"{BASE_URL}/health/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

    return response.status_code == 200


def test_create_booking():
    """Тест создания бронирования"""
    print("\n🔍 Тест 2: Создание бронирования")
    print("-" * 50)

    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    booking_data = {
        "user_email": "test@example.com",
        "room_number": "101",
        "booking_date": tomorrow,
        "start_time": "10:00",
        "end_time": "12:00",
        "booking_type": "lesson",
        "purpose": "Тестовое бронирование"
    }

    print(f"Отправка данных:")
    print(json.dumps(booking_data, indent=2, ensure_ascii=False))

    response = requests.post(
        f"{BASE_URL}/create-booking/",
        json=booking_data,
        headers={"Content-Type": "application/json"}
    )

    print(f"\nStatus Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

    return response.status_code == 201


def test_list_bookings():
    """Тест получения списка бронирований"""
    print("\n🔍 Тест 3: Список бронирований")
    print("-" * 50)

    response = requests.get(f"{BASE_URL}/bookings/")
    print(f"Status Code: {response.status_code}")
    print(f"Количество бронирований: {len(response.json())}")

    if response.json():
        print(f"\nПервое бронирование:")
        print(json.dumps(response.json()[0], indent=2, ensure_ascii=False))

    return response.status_code == 200


def test_get_stats():
    """Тест получения статистики"""
    print("\n🔍 Тест 4: Статистика")
    print("-" * 50)

    response = requests.get(f"{BASE_URL}/bookings/stats/")
    print(f"Status Code: {response.status_code}")
    print(f"Статистика:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

    return response.status_code == 200


def run_all_tests():
    """Запуск всех тестов"""
    print("=" * 50)
    print("🚀 ЗАПУСК ТЕСТОВ API")
    print("=" * 50)

    results = []

    try:
        results.append(("Health Check", test_health_check()))
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        results.append(("Health Check", False))

    try:
        results.append(("Создание бронирования", test_create_booking()))
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        results.append(("Создание бронирования", False))

    try:
        results.append(("Список бронирований", test_list_bookings()))
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        results.append(("Список бронирований", False))

    try:
        results.append(("Статистика", test_get_stats()))
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        results.append(("Статистика", False))

    # Итоги
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТОВ")
    print("=" * 50)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\nИтого: {passed}/{total} тестов пройдено")

    if passed == total:
        print("\n🎉 Все тесты успешно пройдены!")
    else:
        print("\n⚠️ Некоторые тесты не прошли")


if __name__ == "__main__":
    print("""
    ⚙️ ИНСТРУКЦИЯ:
    1. Убедитесь, что сервер запущен: python manage.py runserver
    2. Запустите этот скрипт: python test_api.py
    3. Проверьте результаты тестов

    📝 ПРИМЕЧАНИЕ:
    - Если сервис доступности (Студент B) не запущен,
      бронирования будут создаваться со статусом 'rejected'
    """)

    input("Нажмите Enter для запуска тестов...")

    run_all_tests()