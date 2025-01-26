from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from config.settings import NULLABLE
from users.models import User

class Client(models.Model):
    email = models.OneToOneField('users.User', on_delete=models.CASCADE, verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    gender = models.CharField(max_length=1, verbose_name='Пол', choices=(('M', 'Мужской'), ('F', 'Женский')))
    date_of_birth = models.DateField(**NULLABLE, verbose_name='Дата рождения')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

@receiver(post_save, sender=User)
def create_or_update_client(sender, instance, created, **kwargs):
    """Функция создания или обновления клиента. Вызывается при создании или обновлении пользователя."""
    if created:
        Client.objects.create(
            email=instance,
            first_name=instance.first_name,
            last_name=instance.last_name
        )
    else:
        client = Client.objects.filter(email=instance).first()
        if client:
            client.first_name = instance.first_name
            client.last_name = instance.last_name
            client.save()