from django.db import models
from config.settings import NULLABLE


class Doctor(models.Model):
    email = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Email', related_name='doctor_email')
    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    speciality = models.CharField(max_length=150, verbose_name='Специальность', **NULLABLE)
    bio = models.TextField(verbose_name='Биография', **NULLABLE)
    photo = models.ImageField(upload_to='service/photo', verbose_name='Фото', **NULLABLE)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'