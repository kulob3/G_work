import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from appointment.models import Appointment
from clients.models import Client
from service.models import Service

User = get_user_model()

@pytest.mark.django_db
def test_appointment_list_view(client):
    """Тест просмотра списка приемов."""
    user = User.objects.create_user(email='test@example.com', password='password', is_superuser=True)
    client.force_login(user)
    client_obj, _ = Client.objects.get_or_create(email=user)
    service = Service.objects.create(name="Тестовая услуга", price=1500)
    appointment = Appointment.objects.create(
        name="Тестовый прием",
        client=client_obj,
        service=service,
        price=service,
        date="2025-02-01",
        time="12:00:00",
        status="Новый"
    )
    response = client.get(reverse('appointment:appointment_list'))
    content = response.content.decode()
    assert response.status_code == 200
    assert "Запись на прием" in content
    assert "Просмотр" in content


@pytest.mark.django_db
def test_appointment_detail_view(client):
    """Тест просмотра детальной страницы приема."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)
    client_obj, _ = Client.objects.get_or_create(email=user)
    service = Service.objects.create(name="Тестовая услуга", price=1500)
    appointment = Appointment.objects.create(
        name="Тестовый прием",
        client=client_obj,
        service=service,
        price=service,
        date="2025-02-01",
        time="12:00:00",
        status="Новый"
    )
    response = client.get(reverse('appointment:appointment_view', args=[appointment.pk]))
    assert response.status_code == 200
    assert "Тестовый прием" in response.content.decode()
    assert "Тестовая услуга" in response.content.decode()

@pytest.mark.django_db
def test_appointment_create_view(client):
    """Тест создания нового приема."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)
    client_obj, _ = Client.objects.get_or_create(email=user)
    service = Service.objects.create(name="Тестовая услуга", price=1500)
    form_data = {
        'name': 'Тестовый прием',
        'client': client_obj.pk,
        'service': service.pk,
        'price': service.pk,
        'date': '2025-02-01',
        'time': '12:00:00',
        'status': 'Новый'
    }
    response = client.post(reverse('appointment:appointment_create'), form_data, follow=True)
    assert response.status_code == 200, f"Статус код: {response.status_code}, HTML: {response.content.decode()}"
    appointments = list(Appointment.objects.values())
    print("Все записи в БД:", appointments)
    created_appointment = Appointment.objects.order_by('-id').first()
    assert created_appointment is not None, "Запись не была создана!"
    assert "Запись на прием" in created_appointment.name, f"Неожиданное имя: {created_appointment.name}"

@pytest.mark.django_db
def test_appointment_update_view(client):
    """Тест обновления приема с учетом прав."""
    user = User.objects.create_user(email='test@example.com', password='password', is_superuser=True)
    client.force_login(user)
    client_obj, _ = Client.objects.get_or_create(email=user)
    service = Service.objects.create(name="Консультация", price=2000)
    Appointment.objects.all().delete()
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("ALTER SEQUENCE appointment_appointment_id_seq RESTART WITH 1;")
    appointment = Appointment.objects.create(
        client=client_obj,
        service=service,
        price=service,
        date="2025-02-10",
        time="10:30"
    )
    form_data = {
        'name': appointment.name,
        'client': client_obj.pk,
        'service': service.pk,
        'price': service.pk,
        'date': "2025-02-15",
        'time': "12:00",
        'status': 'confirmed'
    }
    response = client.post(reverse('appointment:appointment_update', args=[appointment.pk]), form_data, follow=True)
    assert response.status_code in [200, 302], f"Ошибка при редактировании: {response.content.decode()}"
    appointment.refresh_from_db()
    assert appointment.date.strftime("%Y-%m-%d") == "2025-02-15", "Дата приема не обновилась!"
    assert appointment.time.strftime("%H:%M") == "12:00", "Время приема не обновилось!"
    assert appointment.status == 'confirmed', "Статус приема не изменился!"



@pytest.mark.django_db
def test_appointment_delete_view(client):
    """Тест удаления приема."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)

    client_obj = Client.objects.create(email=user)
    service = Service.objects.create(name="Лечение", price=3000)
    appointment = Appointment.objects.create(client=client_obj, service=service, date="2025-02-20", time="09:00")

    response = client.post(reverse('appointment:appointment_delete', args=[appointment.pk]), follow=True)

    assert response.status_code == 200
    assert not Appointment.objects.filter(pk=appointment.pk).exists()

