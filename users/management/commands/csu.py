from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email = 'adm@1.ru')
        user.set_password('admin')
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()