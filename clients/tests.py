# import pytest
# from django.db.models.signals import post_save
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from clients.models import Client, create_or_update_client
#
# User = get_user_model()
#
# @pytest.mark.django_db
# def test_client_creation_signal():
#     user = User.objects.create_user(email='test@example.com', password='password', first_name='John', last_name='Doe')
#     client = Client.objects.get(email=user)
#     assert client.first_name == 'John'
#     assert client.last_name == 'Doe'
#
# @pytest.mark.django_db
# def test_client_update_signal():
#     user = User.objects.create_user(email='test@example.com', password='password', first_name='John', last_name='Doe')
#     user.first_name = 'Jane'
#     user.last_name = 'Smith'
#     user.save()
#     client = Client.objects.get(email=user)
#     assert client.first_name == 'Jane'
#     assert client.last_name == 'Smith'
#
# @pytest.mark.django_db
# def test_client_list_view(client):
#     user = User.objects.create_superuser(email='test@example.com', password='password', first_name='John', last_name='Doe')
#     client_instance = Client.objects.get(email=user)  # Получаем клиента, созданного сигналом
#     client.force_login(user)
#     url = reverse('clients:client_list')
#     response = client.get(url)
#     print(response.content.decode())  # Для отладки выводим содержимое страницы
#     assert response.status_code == 200
#     assert 'John Doe' in response.content.decode()  # Проверяем корректное отображение имени
#
#
# @pytest.mark.django_db
# def test_client_detail_view(client):
#     user = User.objects.create_user(
#         email='test@example.com',
#         password='password',
#         first_name='John',
#         last_name='Doe'
#     )
#     client_instance = Client.objects.get(email=user)  # Клиент создан сигналом
#     client_instance.gender = 'M'
#     client_instance.save()  # Обновляем пол
#     client.force_login(user)
#     url = reverse('clients:client_view', args=[client_instance.pk])
#     response = client.get(url)
#     print(response.content.decode())  # Для отладки
#     assert response.status_code == 200
#     assert 'Клиент: John Doe' in response.content.decode()  # Проверяем имя
#     assert 'Мужской' in response.content.decode()  # Проверяем пол
#
#
# @pytest.mark.django_db
# def test_client_update_view(client):
#     user = User.objects.create_user(email='test@example.com', password='password')
#     client_instance = Client.objects.get(email=user)  # Получаем клиента, созданного сигналом
#     client.force_login(user)
#
#     url = reverse('clients:client_edit', args=[client_instance.pk])
#     response = client.post(url, {
#         'first_name': 'Updated John',
#         'last_name': 'Updated Doe',
#         'gender': 'M',
#         'date_of_birth': '1990-01-01',
#         'comment': 'Updated comment'
#     })
#     assert response.status_code == 302  # Проверяем перенаправление
#
#     client_instance.refresh_from_db()
#     assert client_instance.first_name == 'Updated John'
#     assert client_instance.last_name == 'Updated Doe'
#     assert client_instance.comment == 'Updated comment'
#
#
#
#
# @pytest.mark.django_db
# def test_client_delete_view(client):
#     # Создаём пользователя (сигнал автоматически создаст связанного клиента)
#     user = User.objects.create_user(email='test@example.com', password='password')
#
#     # Получаем клиента, созданного сигналом
#     client_instance = Client.objects.get(email=user)
#
#     # Логиним пользователя
#     client.force_login(user)
#
#     # Отправляем запрос на удаление клиента
#     url = reverse('clients:client_delete', args=[client_instance.pk])
#     response = client.post(url)
#
#     # Проверяем статус ответа и отсутствие клиента в базе данных
#     assert response.status_code == 302  # Успешный редирект
#     assert not Client.objects.filter(pk=client_instance.pk).exists()  # Клиент удалён
#
#
# @pytest.mark.django_db
# def test_client_confirm_delete_view(client):
#     # Создаём пользователя (сигнал автоматически создаёт клиента)
#     user = User.objects.create_user(email='test@example.com', password='password', first_name='John', last_name='Doe')
#
#     # Получаем клиента, связанного с пользователем
#     client_instance = Client.objects.get(email=user)
#
#     # Логиним пользователя
#     client.force_login(user)
#
#     # Формируем URL для подтверждения удаления
#     url = reverse('clients:client_delete', args=[client_instance.pk])
#
#     # Проверяем GET-запрос к странице подтверждения удаления
#     response = client.get(url)
#     assert response.status_code == 200
#     assert f'Удалить {client_instance.first_name} {client_instance.last_name}?' in response.content.decode()
#
#     # Отправляем POST-запрос для удаления
#     response = client.post(url)
#     assert response.status_code == 302  # Проверяем успешный редирект после удаления
#     assert not Client.objects.filter(pk=client_instance.pk).exists()  # Проверяем, что клиент удалён
