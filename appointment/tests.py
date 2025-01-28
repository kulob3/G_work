import pytest
from django.contrib.auth import get_user_model
from datetime import date, time
from appointment.models import Appointment
from clients.models import Client
from service.models import Service
from users.models import User


# @pytest.mark.django_db
# class TestAppointmentModel:
#
#     @pytest.fixture(autouse=True)
#     def setup_method(self, db):
#         # Очистка таблиц перед каждым тестом
#         User.objects.all().delete()
#         Client.objects.all().delete()
#         Service.objects.all().delete()
#         Appointment.objects.all().delete()
#
#     def test_appointment_creation(self):
#         """Проверяет создание объекта Appointment"""
#
#         # Создаем пользователя (User), указав поле username, так как оно обязательно
#         user, created = get_user_model().objects.get_or_create(
#             email="test@example.com",
#             defaults={"first_name": "Test", "last_name": "User", "password": "password123"}
#         )
#
#         # Создаем клиента (Client), привязанный к User
#         client, created = Client.objects.get_or_create(
#             email=user,  # Здесь мы передаем объект User, а не 'user'
#             defaults={
#                 "first_name": "Test",
#                 "last_name": "Client",
#                 "gender": "M",
#                 "date_of_birth": date(1990, 1, 1),
#             }
#         )
#
#         # Создаем услугу (Service)
#         service = Service.objects.create(name="Test Service", price=100)
#
#         # Создаем запись о приеме (Appointment)
#         appointment = Appointment.objects.create(
#             client=client,
#             service=service,
#             date=date.today(),
#             time=time(10, 0),
#             status="Новый",
#             price=service  # Ensure price is set to a numeric value
#         )
#
#         # Проверяем корректность строки объекта
#         assert str(appointment) == f"{client} - {appointment.date}"

# @pytest.mark.django_db
# class TestAppointmentViews:
#     def setup_method(self):
#         """Создание данных для тестов"""
#         self.client = Client()
#         self.user = get_user_model().objects.create_user(username="testuser", password="password")
#         self.service = Service.objects.create(name="Test Service", price=100)
#         self.client_model = ClientModel.objects.create(email="testuser@example.com", full_name="Test Client")
#         self.appointment = Appointment.objects.create(
#             client=self.client_model,
#             service=self.service,
#             date=date.today(),
#             time=time(10, 0),
#             status="Новый",
#         )
#
#     def test_appointment_list_view(self):
#         """Тестирует доступ к списку приемов"""
#         self.client.login(username="testuser", password="password")
#         response = self.client.get(reverse("appointment:appointment_list"))
#         assert response.status_code == 200
#         assert "appointment_list" in response.context
#
#     def test_appointment_create_view(self):
#         """Тестирует создание записи на прием"""
#         self.client.login(username="testuser", password="password")
#         data = {
#             "service": self.service.id,
#             "date": date.today(),
#             "time": time(12, 0),
#         }
#         response = self.client.post(reverse("appointment:appointment_create"), data)
#         assert response.status_code == 302  # Redirect to list view
#         assert Appointment.objects.count() == 2  # Новый объект создан
#
#     def test_appointment_update_view(self):
#         """Тестирует обновление записи на прием"""
#         self.client.login(username="testuser", password="password")
#         data = {
#             "service": self.service.id,
#             "date": date.today(),
#             "time": time(14, 0),
#             "status": "Подтвержден",
#         }
#         response = self.client.post(
#             reverse("appointment:appointment_edit", kwargs={"pk": self.appointment.id}),
#             data,
#         )
#         assert response.status_code == 302
#         self.appointment.refresh_from_db()
#         assert self.appointment.status == "Подтвержден"
#
#     def test_appointment_delete_view(self):
#         """Тестирует удаление записи на прием"""
#         self.client.login(username="testuser", password="password")
#         response = self.client.post(
#             reverse("appointment:appointment_delete", kwargs={"pk": self.appointment.id})
#         )
#         assert response.status_code == 302
#         assert Appointment.objects.count() == 0
#
#
# @pytest.mark.django_db
# class TestAppointmentForms:
#     def test_valid_appointment_form(self):
#         """Проверяет корректность формы AppointmentForm"""
#         service = Service.objects.create(name="Test Service", price=100)
#         data = {
#             "service": service.id,
#             "date": date.today(),
#             "time": time(10, 0),
#         }
#         form = AppointmentForm(data=data)
#         assert form.is_valid()
#
#     def test_invalid_appointment_form(self):
#         """Проверяет некорректные данные в форме AppointmentForm"""
#         data = {
#             "date": "invalid_date",
#             "time": "invalid_time",
#         }
#         form = AppointmentForm(data=data)
#         assert not form.is_valid()
