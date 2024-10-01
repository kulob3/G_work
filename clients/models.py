from django.db import models
from config.settings import NULLABLE

class Client(models.Model):
    email = models.EmailField(verbose_name='Email')
    name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'