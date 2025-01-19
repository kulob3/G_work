from django.db import models
from config.settings import NULLABLE


class Doctor(models.Model):
    name = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Имя', related_name='doctor_name')
    first_name = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Имя',
                                   related_name='doctor_first_name', **NULLABLE)
    last_name = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Фамилия',
                                  related_name='doctor_last_name', **NULLABLE)
    speciality = models.CharField(max_length=150, verbose_name='Специальность', **NULLABLE)
    bio = models.TextField(verbose_name='Биография', **NULLABLE)
    photo = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Фото', related_name='doctor_photo',
                              **NULLABLE)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'