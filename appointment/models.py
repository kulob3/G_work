from django.db import models
from config.settings import NULLABLE, APPOINTMENT_STATUS_CHOICES
from doctors.models import Doctor
from service.models import Service


# Функция для default
def default_appointment_name():
    return 'Запись на прием'

class Appointment(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование', default=default_appointment_name)
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, verbose_name='Клиент')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    appointment_number_int = models.IntegerField(verbose_name='Номер записи', null=True)
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    price = models.ForeignKey('service.Service', on_delete=models.CASCADE, verbose_name='Цена', related_name='appointment_prices')
    status = models.CharField(max_length=150, verbose_name='Статус', choices=APPOINTMENT_STATUS_CHOICES, default='Новый')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    result = models.TextField(verbose_name='Результат', **NULLABLE)

    class Meta:
        verbose_name = 'Прием врача'
        verbose_name_plural = 'Прием врачей'

    def __str__(self):
        return f'{self.client} - {self.date}'

    def save(self, *args, **kwargs):
        # Добавляем ID к имени только после сохранения
        if not self.name or self.name == 'Запись на прием':
            super().save(*args, **kwargs)  # Сначала сохраняем объект, чтобы получить ID
            self.name = f'Запись на прием {self.id}'
        super().save(*args, **kwargs)



