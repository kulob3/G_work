# import pytest
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from django.test import Client
#
# User = get_user_model()
#
# @pytest.fixture
# def client():
#     return Client()
#
# @pytest.fixture
# def user_data():
#     return {
#         'email': 'testuser@example.com',
#         'password': 'strongpassword123',
#         'first_name': 'Test',
#         'last_name': 'User',
#         'phone': '+79991234567'
#     }
#
# @pytest.mark.django_db
# def test_user_registration(client, user_data):
#     url = reverse('users:register')
#     response = client.post(url, {
#         'email': user_data['email'],
#         'password1': user_data['password'],
#         'password2': user_data['password'],
#         'first_name': user_data['first_name'],
#         'last_name': user_data['last_name'],
#         'phone': user_data['phone']
#     })
#     print(response.content.decode())  # Для отладки
#     assert response.status_code == 302, f"Expected 302 but got {response.status_code}. Response: {response.content.decode()}"
#     user = User.objects.get(email=user_data['email'])
#     assert not user.is_active
#
#
# @pytest.mark.django_db
# def test_email_verification(client, user_data):
#     user = User.objects.create(**user_data, is_active=False, token='testtoken')
#     url = reverse('users:email-confirm', args=['testtoken'])
#     response = client.get(url)
#     assert response.status_code == 302  # Redirect after verification
#     user.refresh_from_db()
#     assert user.is_active
#
# @pytest.mark.django_db
# def test_password_reset_request(client, user_data):
#     user = User.objects.create_user(**user_data)
#     url = reverse('users:password_reset')
#     response = client.post(url, {'email': user_data['email']})
#     assert response.status_code == 302  # Redirect after success
#
# @pytest.mark.django_db
# def test_user_login(client, user_data):
#     user = User.objects.create_user(**user_data)
#     url = reverse('users:login')
#     response = client.post(url, {
#         'username': user_data['email'],
#         'password': user_data['password']
#     })
#     assert response.status_code == 302  # Successful login
#
# @pytest.mark.django_db
# def test_ban_user(client, user_data):
#     admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpassword')
#     user = User.objects.create_user(**user_data)
#     client.force_login(admin_user)
#     url = reverse('users:ban_user', args=[user.id])
#     response = client.post(url)
#     assert response.status_code == 302  # Redirect after success
#     user.refresh_from_db()
#     assert user.banned
#
# @pytest.mark.django_db
# def test_unban_user(client, user_data):
#     admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpassword')
#     user = User.objects.create_user(**user_data, banned=True)
#     client.force_login(admin_user)
#     url = reverse('users:unban_user', args=[user.id])
#     response = client.post(url)
#     assert response.status_code == 302  # Redirect after success
#     user.refresh_from_db()
#     assert not user.banned
#
#
# @pytest.mark.django_db
# def test_login_page(client):
#     url = reverse('users:login')
#     response = client.get(url)
#     assert response.status_code == 200
#     assert 'Вход в сервис'.encode() in response.content
#
# @pytest.mark.django_db
# def test_password_reset_page(client):
#     url = reverse('users:password_reset')
#     response = client.get(url)
#     assert response.status_code == 200
#     assert 'Сброс пароля'.encode() in response.content
#
# @pytest.mark.django_db
# def test_password_reset_done_page(client):
#     url = reverse('users:password_reset_done')
#     response = client.get(url)
#     assert response.status_code == 200
#     assert 'Инструкции по сбросу пароля были отправлены на почту'.encode() in response.content
#
# @pytest.mark.django_db
# def test_register_page(client):
#     url = reverse('users:register')
#     response = client.get(url)
#     assert response.status_code == 200
#     assert 'Регистрация в сервисе'.encode() in response.content
#
# @pytest.mark.django_db
# def test_user_list_page(client):
#     admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpassword')
#     client.force_login(admin_user)
#     url = reverse('users:user_list')
#     response = client.get(url)
#     assert response.status_code == 200
#     assert 'У вас нет прав для просмотра информации на этой странице'.encode() not in response.content
#
# @pytest.mark.django_db
# def test_user_list_page_no_permissions(client):
#     regular_user = User.objects.create_user(email='user@example.com', password='userpassword')
#     client.force_login(regular_user)
#     url = reverse('users:user_list')
#     response = client.get(url)
#     assert response.status_code == 200
#     assert 'У вас нет прав для просмотра информации на этой странице'.encode() in response.content