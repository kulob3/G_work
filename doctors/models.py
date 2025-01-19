from django.db import models
from config.settings import NULLABLE


class Doctor(models.Model):
    email = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Email', related_name='doctor_email')
    first_name = models.CharField(max_length=150, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', null=True, blank=True)
    speciality = models.CharField(max_length=150, verbose_name='Специальность', null=True, blank=True)
    bio = models.TextField(verbose_name='Биография', null=True, blank=True)
    photo = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Фото', related_name='doctor_photo', null=True, blank=True)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'