from django.core.management.base import BaseCommand
from sending.models import MailingStatus


class Command(BaseCommand):
    """Осуществляет запуск рассылок посредством установки флага is_running в True"""

    def handle(self, *args, **kwargs):
        status, created = MailingStatus.objects.get_or_create(id=1)
        status.is_running = True
        status.save()
        self.stdout.write(self.style.SUCCESS('Рассылка запущена'))