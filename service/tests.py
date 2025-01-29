import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from service.models import Service

User = get_user_model()

@pytest.mark.django_db
def test_service_list_view(client):
    """Тест просмотра списка услуг."""
    user = User.objects.create_user(email='test@example.com', password='password', is_superuser=True)
    client.force_login(user)
    response = client.get(reverse('service:service_list'))
    assert response.status_code == 200
    assert "Создать новую услугу" in response.content.decode()

@pytest.mark.django_db
def test_service_detail_view(client):
    """Тест просмотра детальной страницы услуги."""
    user = User.objects.create_user(email='test@example.com', password='password')
    service = Service.objects.create(name="Тестовая услуга", description="Описание услуги", price=1000)
    client.force_login(user)
    response = client.get(reverse('service:service_view', args=[service.pk]))
    assert response.status_code == 200
    assert "Тестовая услуга" in response.content.decode()

@pytest.mark.django_db
def test_service_create_view(client):
    """Тест создания новой услуги."""
    user = User.objects.create_user(email='test@example.com', password='password', is_superuser=True)
    client.force_login(user)
    response = client.post(reverse('service:service_create'), {
        'name': 'Новая услуга',
        'description': 'Описание новой услуги',
        'price': 1500
    })
    assert response.status_code == 302
    assert Service.objects.filter(name='Новая услуга').exists()

@pytest.mark.django_db
def test_service_update_view(client):
    """Тест обновления услуги."""
    user = User.objects.create_user(email='test@example.com', password='password', is_superuser=True)
    client.force_login(user)
    service = Service.objects.create(name="Услуга для редактирования", description="Описание", price=2000)
    response = client.post(reverse('service:service_edit', args=[service.pk]), {
        'name': 'Обновленная услуга',
        'description': 'Обновленное описание',
        'price': 2500
    })
    assert response.status_code == 302
    service.refresh_from_db()
    assert service.name == 'Обновленная услуга'

@pytest.mark.django_db
def test_service_delete_view(client):
    """Тест удаления услуги."""
    user = User.objects.create_user(email='test@example.com', password='password', is_superuser=True)
    service = Service.objects.create(name="Услуга для удаления", description="Описание", price=3000)
    client.force_login(user)
    response = client.post(reverse('service:service_delete', args=[service.pk]), follow=True)
    assert response.status_code == 200
    assert not Service.objects.filter(pk=service.pk).exists()

@pytest.mark.django_db
def test_http_service_detail_view(client):
    """Тест HTTP-запроса на просмотр страницы услуги."""
    user = User.objects.create_user(email='test@example.com', password='password')
    service = Service.objects.create(name="HTTP Тестовая услуга", description="Описание HTTP", price=1200)
    client.force_login(user)
    response = client.get(reverse('service:service_view', args=[service.pk]))
    assert response.status_code == 200
    assert "HTTP Тестовая услуга" in response.content.decode()

@pytest.mark.django_db
def test_http_service_create_view(client):
    """Тест HTTP-запроса на создание новой услуги."""
    user = User.objects.create_user(email='test@example.com', password='password', is_superuser=True)
    client.force_login(user)
    response = client.post(reverse('service:service_create'), {
        'name': 'HTTP Новая услуга',
        'description': 'HTTP Описание услуги',
        'price': 1800
    })
    if response.status_code == 200:
        print("Ошибки формы:", response.context['form'].errors)
    assert response.status_code == 302
    assert Service.objects.filter(name='HTTP Новая услуга').exists()


