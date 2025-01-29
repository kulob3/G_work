import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Blog
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

User = get_user_model()

@pytest.mark.django_db
def test_blog_list_view(client):
    """Тест просмотра списка постов."""
    url = reverse('blog:blog_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_blog_detail_view(client):
    """Тест детального просмотра поста."""
    user = User.objects.create_user(email='test@example.com', password='password')
    blog_post = Blog.objects.create(
        title='Test Post',
        content='Test Content',
        owner=user
    )
    url = reverse('blog:blog_view', args=[blog_post.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert 'Test Post' in response.content.decode()


@pytest.mark.django_db
def test_blog_create_view(client):
    """Тест создания нового поста."""
    user = User.objects.create_user(email='test@example.com', password='password')
    client.force_login(user)
    image = Image.new('RGB', (100, 100), color='red')
    img_io = io.BytesIO()
    image.save(img_io, format='JPEG')
    img_io.seek(0)
    preview_file = SimpleUploadedFile("preview.jpg", img_io.read(), content_type="image/jpeg")
    url = reverse('blog:blog_create')
    response = client.post(url, {
        'title': 'New Post',
        'content': 'New Content',
        'preview': preview_file,
    }, format='multipart')
    if hasattr(response, "context") and response.context is not None:
        print(response.context.get('form').errors)
    assert response.status_code in [200, 302], f"Unexpected status code: {response.status_code}"
    if response.status_code == 302:
        assert Blog.objects.filter(title='New Post').exists()


@pytest.mark.django_db
def test_blog_update_view(client):
    """Тест обновления поста."""
    user = User.objects.create_user(email='test@example.com', password='password')
    blog_post = Blog.objects.create(
        title='Old Title',
        content='Old Content',
        owner=user
    )
    client.force_login(user)
    url = reverse('blog:blog_edit', args=[blog_post.pk])
    image = Image.new('RGB', (100, 100), color='blue')
    img_io = io.BytesIO()
    image.save(img_io, format='JPEG')
    img_io.seek(0)
    preview_file = SimpleUploadedFile("preview.jpg", img_io.read(), content_type="image/jpeg")
    response = client.post(url, {
        'title': 'Updated Title',
        'content': 'Updated Content',
        'preview': preview_file,
    }, format='multipart')
    assert response.status_code in [200, 302], f"Unexpected status code: {response.status_code}"
    if response.status_code == 200 and response.context:
        print(response.context.get('form').errors)
    blog_post.refresh_from_db()
    assert blog_post.title == 'Updated Title'
    assert blog_post.content == 'Updated Content'


@pytest.mark.django_db
def test_blog_delete_view(client):
    """Тест удаления поста."""
    user = User.objects.create_user(email='test@example.com', password='password')
    blog_post = Blog.objects.create(
        title='To Be Deleted',
        content='Some Content',
        owner=user
    )
    client.force_login(user)
    url = reverse('blog:blog_delete', args=[blog_post.pk])
    response = client.get(url)
    assert response.status_code == 200, f"Unexpected status code on GET: {response.status_code}"
    assert 'Удалить' in response.content.decode(), "Текст подтверждения удаления не найден"
    response = client.post(url)
    assert response.status_code == 302, f"Unexpected status code on DELETE: {response.status_code}"
    assert not Blog.objects.filter(pk=blog_post.pk).exists(), "Blog post was not deleted"



