import pytest
from django.urls import reverse
from message.models import Message
from users.models import User


@pytest.mark.django_db
def test_message_list_view(client):
    """Тест просмотра списка сообщений с HTML-проверкой."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)

    Message.objects.create(topic="Первое сообщение", owner=user)
    Message.objects.create(topic="Второе сообщение", owner=user)

    response = client.get(reverse('message:message_list'))

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    content = response.content.decode()
    assert "Создать новое сообщение" in content, "Кнопка создания сообщения отсутствует"
    assert "Первое сообщение" in content, "Первое сообщение отсутствует в списке"
    assert "Второе сообщение" in content, "Второе сообщение отсутствует в списке"


@pytest.mark.django_db
def test_message_detail_view(client):
    """Тест просмотра страницы сообщения с HTML-проверкой."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)

    # Создаём объект сообщения
    message = Message.objects.create(
        topic='Тестовая тема',
        body='Тестовый контент',
        owner=user
    )
    response = client.get(reverse('message:message_view', args=[message.pk]))
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    content = response.content.decode()
    assert "Тестовая тема" in content, "Тема сообщения не отображается"
    assert "Тестовый контент" in content, "Содержимое сообщения не отображается"
    assert f"{user.email}" in content, "Имя владельца сообщения не отображается"

@pytest.mark.django_db
def test_message_create_view(client):
    """Тест создания сообщения с проверкой HTML."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)
    url = reverse('message:message_create')
    response = client.post(url, {
        'topic': 'Новое сообщение',
        'body': 'Содержимое нового сообщения'
    })
    if response.status_code == 200 and response.context and 'form' in response.context:
        print(response.context['form'].errors)
    assert response.status_code == 302, f"Unexpected status code: {response.status_code}"
    assert Message.objects.filter(topic='Новое сообщение').exists(), "Сообщение не было создано"


@pytest.mark.django_db
def test_message_update_view(client):
    """Тест обновления сообщения."""
    user = User.objects.create_user(email='test@example.com', password='password')
    message = Message.objects.create(topic='Старый заголовок', body='Старый текст', owner=user)
    client.force_login(user)
    url = reverse('message:message_edit', args=[message.pk])
    response = client.post(url, {
        'topic': 'Обновленный заголовок',
        'body': 'Обновленный текст'
    })
    assert response.status_code == 302, f"Unexpected status code: {response.status_code}"
    message.refresh_from_db()
    assert message.topic == 'Обновленный заголовок'
    assert message.body == 'Обновленный текст'

@pytest.mark.django_db
def test_message_delete_view(client):
    """Тест удаления сообщения."""
    user = User.objects.create_user(email='test@example.com', password='password')
    message = Message.objects.create(topic='Удалить меня', body='Тест', owner=user)
    client.force_login(user)
    url = reverse('message:message_delete', args=[message.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert f"<h4>Удалить {message.topic}?</h4>" in response.content.decode()
    response = client.post(url)
    assert response.status_code == 302
    assert not Message.objects.filter(pk=message.pk).exists()



