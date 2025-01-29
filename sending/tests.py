import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from sending.models import Sending
from message.models import Message
from clients.models import Client

User = get_user_model()

@pytest.mark.django_db
def test_sending_list_view(client):
    """Тест просмотра списка рассылок с HTML проверкой."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)
    response = client.get(reverse('sending:sending_list'))
    assert response.status_code == 200
    assert "Список рассылок" in response.content.decode()

@pytest.mark.django_db
def test_sending_detail_view(client):
    """Тест просмотра страницы рассылки."""
    user = User.objects.create_user(email='test@example.com', password='password')
    message = Message.objects.create(topic='Тестовое сообщение', body='Текст сообщения', owner=user)
    sending = Sending.objects.create(name='Тестовая рассылка', owner=user, message=message, period='daily')
    sending.clients.set([])
    client.force_login(user)
    response = client.get(reverse('sending:sending_view', args=[sending.pk]))
    assert response.status_code == 200
    assert "Тестовая рассылка" in response.content.decode()

@pytest.mark.django_db
def test_sending_create_view(client, db):
    """Тест создания новой рассылки."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)
    message = Message.objects.create(topic='Тестовое сообщение', body='Текст сообщения', owner=user)
    client_user = User.objects.create_user(email='client@example.com', password='password')
    client_obj, _ = Client.objects.get_or_create(email=client_user)
    print(f"Создан клиент: {client_obj.pk}, email: {client_obj.email}")  # Отладка
    response_form = client.get(reverse('sending:sending_create'))
    available_clients = list(response_form.context['form'].fields['clients'].queryset.values_list('pk', flat=True))
    print(f"Доступные клиенты в форме: {available_clients}")
    if available_clients:
        selected_client = available_clients[0]
    else:
        selected_client = client_obj.pk
    response = client.post(reverse('sending:sending_create'), {
        'name': 'Новая рассылка',
        'message': message.pk,
        'period': 'daily',
        'status': 'created',
        'number_of_parcels': 1,
        'clients': [selected_client]
    })
    assert response.status_code in [200, 302]
    if response.status_code == 200:
        print("Ошибки формы:", response.context['form'].errors)
    sending = Sending.objects.filter(name='Новая рассылка').first()
    assert sending is not None
    sending.owner = user
    sending.clients.set([selected_client])
    sending.save()

@pytest.mark.django_db
def test_sending_update_view(client):
    """Тест редактирования рассылки."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)
    message = Message.objects.create(topic='Тестовое сообщение', body='Текст сообщения', owner=user)
    sending = Sending.objects.create(name='Редактируемая рассылка', owner=user, message=message, period='weekly')
    sending.clients.set([])
    client_user = User.objects.create_user(email='client@example.com', password='password')
    client_obj, created = Client.objects.get_or_create(email=client_user)
    response = client.post(reverse('sending:sending_edit', args=[sending.pk]), {
        'name': 'Обновленная рассылка',
        'message': message.pk,
        'period': 'weekly',
        'status': 'created',
        'clients': [client_obj.pk],
        'number_of_parcels': 1
    })
    assert response.status_code == 302
    sending.refresh_from_db()
    assert sending.name == 'Обновленная рассылка'

@pytest.mark.django_db
def test_sending_delete_view(client):
    """Тест удаления рассылки."""
    user = User.objects.create_user(email='test@example.com', password='password')
    message = Message.objects.create(topic='Тестовое сообщение', body='Текст сообщения', owner=user)
    sending = Sending.objects.create(name='Удаляемая рассылка', owner=user, message=message, period='monthly')
    client.force_login(user)
    response = client.post(reverse('sending:sending_delete', args=[sending.pk]), follow=True)
    assert response.status_code == 200
    assert not Sending.objects.filter(pk=sending.pk).exists()

@pytest.mark.django_db
def test_http_sending_list_view(client):
    """Тест HTTP-запроса на просмотр списка рассылок."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)
    response = client.get(reverse('sending:sending_list'))
    assert response.status_code == 200
    assert "Список рассылок" in response.content.decode()

@pytest.mark.django_db
def test_http_sending_detail_view(client):
    """Тест HTTP-запроса на просмотр страницы рассылки."""
    user = User.objects.create_user(email='test@example.com', password='password')
    message = Message.objects.create(topic='Тестовое сообщение', body='Текст сообщения', owner=user)
    sending = Sending.objects.create(name='Тестовая рассылка', owner=user, message=message, period='daily')
    sending.clients.set([])
    client.force_login(user)
    response = client.get(reverse('sending:sending_view', args=[sending.pk]))
    assert response.status_code == 200
    assert "Тестовая рассылка" in response.content.decode()

@pytest.mark.django_db
def test_http_sending_create_view(client):
    """Тест HTTP-запроса на создание новой рассылки."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)
    message = Message.objects.create(topic='Тестовое сообщение', body='Текст сообщения', owner=user)
    client_obj, _ = Client.objects.get_or_create(email=user)
    response = client.post(reverse('sending:sending_create'), {
        'name': 'Новая рассылка',
        'message': message.pk,
        'period': 'daily',
        'status': 'created',
        'number_of_parcels': 1,
        'clients': [client_obj.pk]
    })
    if response.status_code == 200:
        print("Ошибки формы:", response.context['form'].errors)
    assert response.status_code == 302
    assert Sending.objects.filter(name='Новая рассылка').exists()


@pytest.mark.django_db
def test_http_sending_update_view(client):
    """Тест HTTP-запроса на обновление рассылки."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)
    message = Message.objects.create(topic='Тестовое сообщение', body='Текст сообщения', owner=user)
    sending = Sending.objects.create(name='Редактируемая рассылка', owner=user, message=message, period='weekly')
    sending.clients.set([])
    client_user = User.objects.create_user(email='client@example.com', password='password')
    client_obj, _ = Client.objects.get_or_create(email=client_user)
    response = client.post(reverse('sending:sending_edit', args=[sending.pk]), {
        'name': 'Обновленная рассылка',
        'message': message.pk,
        'period': 'weekly',
        'status': 'created',
        'number_of_parcels': 1,
        'clients': [client_obj.pk]
    })
    assert response.status_code == 302
    sending.refresh_from_db()
    assert sending.name == 'Обновленная рассылка'

@pytest.mark.django_db
def test_http_sending_delete_view(client):
    """Тест HTTP-запроса на удаление рассылки."""
    user = User.objects.create_user(email='test@example.com', password='password')
    message = Message.objects.create(topic='Тестовое сообщение', body='Текст сообщения', owner=user)
    sending = Sending.objects.create(name='Удаляемая рассылка', owner=user, message=message, period='monthly')
    client.force_login(user)
    response = client.post(reverse('sending:sending_delete', args=[sending.pk]), follow=True)
    assert response.status_code == 200
    assert not Sending.objects.filter(pk=sending.pk).exists()



