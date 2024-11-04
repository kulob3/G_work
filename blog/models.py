from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок', help_text='Введите заголовок блога')
    slug = models.SlugField(max_length=150, verbose_name='Slug')
    content = models.TextField(verbose_name='Содержание', help_text='Введите содержание блога')
    preview = models.ImageField(upload_to='blog/photo', verbose_name='Изображение', help_text='Загрузите изображение')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец', related_name='blog', editable=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['title']
