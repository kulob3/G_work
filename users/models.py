from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from config.settings import NULLABLE, MANAGER_PERMISSIONS


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    phone = PhoneNumberField(unique=True, verbose_name='Номер телефона', **NULLABLE)
    avatar = models.ImageField(verbose_name='Фото', upload_to='users/avatars/', **NULLABLE)
    token = models.CharField(max_length=150, verbose_name='token', **NULLABLE)
    banned = models.BooleanField(default=False, verbose_name='Пользователь забанен')
    is_manager = models.BooleanField(default=False, verbose_name='Менеджер')
    is_client = models.BooleanField(default=False, verbose_name='Клиент')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        permissions = MANAGER_PERMISSIONS

    def __str__(self):
        return self.email
