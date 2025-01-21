from django.db import models
from config.settings import NULLABLE


class Service(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', **NULLABLE)
    duration = models.DurationField(verbose_name='Продолжительность', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'