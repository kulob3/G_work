import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from clients.models import Client

User = get_user_model()

@pytest.mark.django_db
def test_client_creation_signal():
    user = User.objects.create_user(email='test@example.com', password='password', first_name='John', last_name='Doe')
    client = Client.objects.get(email=user)
    assert client.first_name == 'John'
    assert client.last_name == 'Doe'

@pytest.mark.django_db
def test_client_update_signal():
    user = User.objects.create_user(email='test@example.com', password='password', first_name='John', last_name='Doe')
    user.first_name = 'Jane'
    user.last_name = 'Smith'
    user.save()
    client = Client.objects.get(email=user)
    assert client.first_name == 'Jane'
    assert client.last_name == 'Smith'

@pytest.mark.django_db
def test_client_list_view(client):
    user = User.objects.create_superuser(email='test@example.com', password='password', first_name='John', last_name='Doe')
    client_instance = Client.objects.get(email=user)
    client.force_login(user)
    url = reverse('clients:client_list')
    response = client.get(url)
    print(response.content.decode())
    assert response.status_code == 200
    assert 'John Doe' in response.content.decode()

@pytest.mark.django_db
def test_client_detail_view(client):
    user = User.objects.create_user(
        email='test@example.com',
        password='password',
        first_name='John',
        last_name='Doe'
    )
    client_instance = Client.objects.get(email=user)
    client_instance.gender = 'M'
    client_instance.save()
    client.force_login(user)
    url = reverse('clients:client_view', args=[client_instance.pk])
    response = client.get(url)
    print(response.content.decode())
    assert response.status_code == 200
    assert 'Клиент: John Doe' in response.content.decode()
    assert 'Мужской' in response.content.decode()

@pytest.mark.django_db
def test_client_update_view(client):
    user = User.objects.create_user(email='test@example.com', password='password')
    client_instance = Client.objects.get(email=user)
    client.force_login(user)
    url = reverse('clients:client_edit', args=[client_instance.pk])
    response = client.post(url, {
        'first_name': 'Updated John',
        'last_name': 'Updated Doe',
        'gender': 'M',
        'date_of_birth': '1990-01-01',
        'comment': 'Updated comment'
    })
    assert response.status_code == 302
    client_instance.refresh_from_db()
    assert client_instance.first_name == 'Updated John'
    assert client_instance.last_name == 'Updated Doe'
    assert client_instance.comment == 'Updated comment'

@pytest.mark.django_db
def test_client_delete_view(client):
    user = User.objects.create_user(email='test@example.com', password='password')
    client_instance = Client.objects.get(email=user)
    client.force_login(user)
    url = reverse('clients:client_delete', args=[client_instance.pk])
    response = client.post(url)
    assert response.status_code == 302
    assert not Client.objects.filter(pk=client_instance.pk).exists()

@pytest.mark.django_db
def test_client_confirm_delete_view(client):
    user = User.objects.create_user(email='test@example.com', password='password', first_name='John', last_name='Doe')
    client_instance = Client.objects.get(email=user)
    client.force_login(user)
    url = reverse('clients:client_delete', args=[client_instance.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert f'Удалить {client_instance.first_name} {client_instance.last_name}?' in response.content.decode()
    response = client.post(url)
    assert response.status_code == 302
    assert not Client.objects.filter(pk=client_instance.pk).exists()
