import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from doctors.models import Doctor
from users.models import User


@pytest.mark.django_db
def test_doctor_list_view(client):
    """Тест просмотра списка врачей с проверкой HTML."""
    Doctor.objects.create(first_name='Анна', last_name='Иванова', speciality='Терапевт')
    Doctor.objects.create(first_name='Олег', last_name='Сидоров', speciality='Кардиолог')
    response = client.get(reverse('doctors:doctor_list'))
    assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
    content = response.content.decode()
    assert '<div class="doctor-list">' in content, "На странице отсутствует контейнер списка врачей"
    assert 'Анна Иванова' in content, "На странице отсутствует первый врач"
    assert 'Олег Сидоров' in content, "На странице отсутствует второй врач"
    assert 'Просмотр' in content, "На странице нет кнопки просмотра врача"
    if response.wsgi_request.user.is_authenticated and response.wsgi_request.user.is_superuser:
        assert 'Создать нового врача' in content, "На странице отсутствует кнопка создания врача для администратора"

@pytest.mark.django_db
def test_doctor_detail_view(client):
    """Тест просмотра страницы врача."""
    doctor = Doctor.objects.create(
        first_name='Иван', last_name='Иванов', speciality='Хирург',
        bio='Опытный хирург', photo=None
    )
    response = client.get(reverse('doctors:doctor_view', args=[doctor.pk]))
    assert response.status_code == 200
    content = response.content.decode()
    assert 'Данные врача: Иван Иванов' in content
    assert 'Специальность: Хирург' in content
    assert 'Опыт работы: Опытный хирург' in content
    assert 'Редактировать' not in content
    assert 'Удалить' not in content
    assert 'Назад' in content


@pytest.mark.django_db
def test_doctor_create_view(client):
    """Тест создания врача с проверкой HTML."""
    user = User.objects.create_user(email='admin@example.com', password='password')
    client.force_login(user)
    url = reverse('doctors:doctor_create')
    response = client.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    assert "Создание нового врача" in content, "Не найден заголовок формы"
    assert '<form method="post"' in content, "Форма не найдена в HTML"
    assert 'name="first_name"' in content, "Поле 'Имя' отсутствует"
    assert 'name="last_name"' in content, "Поле 'Фамилия' отсутствует"
    assert 'name="speciality"' in content, "Поле 'Специальность' отсутствует"
    assert 'name="bio"' in content, "Поле 'Биография' отсутствует"
    assert 'name="photo"' in content, "Поле 'Фото' отсутствует"
    image = Image.new('RGB', (100, 100), color='red')
    img_io = io.BytesIO()
    image.save(img_io, format='JPEG')
    img_io.seek(0)
    photo = SimpleUploadedFile("photo.jpg", img_io.read(), content_type="image/jpeg")
    response = client.post(url, {
        'first_name': 'Анна',
        'last_name': 'Петрова',
        'speciality': 'Терапевт',
        'bio': 'Хороший специалист',
        'photo': photo
    }, format='multipart')
    assert response.status_code == 302, "После успешного создания врача должен быть редирект"
    assert Doctor.objects.filter(first_name="Анна", last_name="Петрова").exists(), "Врач не был создан"


@pytest.mark.django_db
def test_doctor_update_view(client):
    """Тест обновления данных врача с проверкой HTML."""
    user = User.objects.create_user(email='admin@example.com', password='password')
    doctor = Doctor.objects.create(first_name='Олег', last_name='Сидоров', speciality='Кардиолог')
    client.force_login(user)
    url = reverse('doctors:doctor_edit', args=[doctor.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert "Редактирование врача" in response.content.decode(), response.content.decode()
    response = client.post(url, {
        'first_name': 'Олег',
        'last_name': 'Сидоров',
        'speciality': 'Невролог'
    })
    assert response.status_code == 302
    doctor.refresh_from_db()
    assert doctor.speciality == 'Невролог'

@pytest.mark.django_db
def test_doctor_delete_view(client):
    """Тест удаления врача с проверкой HTML."""
    user = User.objects.create_user(email='admin@example.com', password='password')
    doctor = Doctor.objects.create(first_name='Михаил', last_name='Козлов', speciality='Офтальмолог')
    client.force_login(user)
    url = reverse('doctors:doctor_delete', args=[doctor.pk])
    response = client.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    assert f"Удалить {doctor.first_name} {doctor.last_name}?" in content
    assert '<button type="submit" class="btn btn-primary">Да</button>' in content
    assert f'<a class="btn btn-primary" href="{reverse("doctors:doctor_view", args=[doctor.pk])}">Нет</a>' in content
    response = client.post(url)
    assert response.status_code == 302
    assert not Doctor.objects.filter(pk=doctor.pk).exists()
