# sending/services.py
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
import pytz

from sending.models import Sending

def send_mailing(pytz=pytz):
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    # создание объекта с применением фильтра
    mailings = Sending.objects.filter(datetime__lte=current_datetime).filter(
        status__in=[status for status, _ in settings.STATUS_CHOICES])

    for mailing in mailings:
        send_mail(
            subject=mailing.message.topic,
            message=mailing.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.clients.all()]
        )