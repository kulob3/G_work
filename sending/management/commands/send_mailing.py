from django.core.management.base import BaseCommand
from sending.services import send_mailing

class Command(BaseCommand):
    help = 'Send mailing'

    def handle(self, *args, **kwargs):
        send_mailing()
        self.stdout.write(self.style.SUCCESS('Successfully sent mailings'))