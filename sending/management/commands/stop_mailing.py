from django.core.management.base import BaseCommand
from sending.models import MailingStatus

class Command(BaseCommand):
    """Осуществляет остановку рассылок посредством установки флага is_running в False"""
    def handle(self, *args, **kwargs):
        status, created = MailingStatus.objects.get_or_create(id=1)
        status.is_running = False
        status.save()
        self.stdout.write(self.style.SUCCESS('Рассылка остановлена'))