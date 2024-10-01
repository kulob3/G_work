from django.db import models
from datetime import datetime, timedelta
from config.settings import PERIOD_CHOICES, STATUS_CHOICES
from config.settings import NULLABLE
from clients.models import Client



class Sending(models.Model):
    def default_sending_name():
        return 'Рассылка от ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    name = models.CharField(max_length=150, verbose_name='Название рассылки', default=default_sending_name)
    datetime = models.DateTimeField(verbose_name='Дата и время первой отправки', auto_now_add=True)
    period = models.CharField(max_length=50, choices=PERIOD_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='Статус рассылки')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    message = models.ForeignKey('message.Message', on_delete=models.CASCADE, verbose_name='Сообщение')
    number_of_parcels = models.IntegerField(verbose_name='Количество писем', default=1)

    def calculate_next_datetime(self):
        if self.period == 'minute':
            return self.datetime + timedelta(minutes=1)
        elif self.period == 'daily':
            return self.datetime + timedelta(days=1)
        elif self.period == 'weekly':
            return self.datetime + timedelta(weeks=1)
        elif self.period == 'monthly':
            return self.datetime + timedelta(days=30)
        return self.datetime

    def __str__(self):
        return f"{self.datetime} {self.status}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'



class SendAttempt(models.Model):
    datetime = models.DateTimeField(verbose_name='Дата и время попытки', db_index=True)
    status = models.BooleanField(verbose_name='Статус попытки')
    response = models.TextField(**NULLABLE, verbose_name='Ответ почтового сервера')
    sending = models.ForeignKey(Sending, on_delete=models.CASCADE, related_name='attempts', verbose_name='Рассылка', default=1)
    story_attempt = models.TextField(verbose_name='История попыток', default='Не было рассылки пока')

    def __str__(self):
        return f"{self.datetime} {self.status}"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

