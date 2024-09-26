from django.db import models
from datetime import datetime, timedelta
from config.settings import PERIOD_CHOICES, STATUS_CHOICES

NULLABLE = {'null': True, 'blank': True}

# Сущности системы
# Клиент сервиса:
# контактный email,
# Ф. И. О.,
# комментарий.
# Обратите внимание, что клиенты сервиса — это не пользователи сервиса. Клиенты — это те, кто получает рассылки, а пользователи — те, кто создает эти рассылки.
#
# Клиенты — неотъемлемая часть рассылки. Для них также необходимо реализовать CRUD-механизм!
#
# Рассылка (настройки):
# дата и время первой отправки рассылки;
# периодичность: раз в день, раз в неделю, раз в месяц;
# статус рассылки (например, завершена, создана, запущена).
# Рассылка внутри себя должна содержать ссылки на модели «Сообщения» и «Клиенты сервиса». Сообщение у рассылки может быть только одно, а вот клиентов может быть много. Выберите правильные типы связи между моделями.
#
# Пример: компания N захотела создать на нашем сервисе рассылку. Создала для нее сообщение, которое будет отправлено клиентам, наполнила базу клиентов своими данными с помощью графического интерфейса сайта, затем перешла к созданию рассылки: указала необходимые параметры, сообщение и выбрала клиентов, которым эта рассылка должна быть отправлена.
#
# Сообщение для рассылки:
# тема письма,
# тело письма.
# Сообщения — неотъемлемая часть рассылки. Для них также необходимо реализовать CRUD-механизм!
#
# Попытка рассылки:
# дата и время последней попытки;
# статус попытки (успешно / не успешно);
# ответ почтового сервера, если он был.

class Client(models.Model):
    email = models.EmailField(verbose_name='Email')
    name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Sending(models.Model):
    datetime = models.DateTimeField(verbose_name='Дата и время первой отправки', auto_now_add=True)
    period = models.CharField(max_length=50, choices=PERIOD_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='Статус рассылки')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='Сообщение')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.datetime = self.calculate_datetime()
        super().save(*args, **kwargs)

    def calculate_datetime(self):
        now = datetime.now()
        if self.period == 'minute':
            return now + timedelta(minutes=1)
        elif self.period == 'daily':
            return now + timedelta(days=1)
        elif self.period == 'weekly':
            return now + timedelta(weeks=1)
        elif self.period == 'monthly':
            return now + timedelta(days=30)
        return now

    def __str__(self):
        return f"{self.datetime} {self.status}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

class Message(models.Model):
    topic = models.CharField(max_length=150, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Содержание письма')

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

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

