import time
import logging
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
import pytz
from sending.models import Sending, SendAttempt

logger = logging.getLogger(__name__)

def send_mailing(pytz=pytz):
    print("Рассылки запущены")
    while True:
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)

        # Фильтрация рассылок по дате и статусу "started"
        mailings = Sending.objects.filter(
            datetime__lte=current_datetime,
            status='started'
        )

        for mailing in mailings:
            # Проверка, что количество отправленных писем меньше допустимого числа
            if mailing.attempts.count() < mailing.number_of_parcels:
                try:
                    send_mail(
                        subject=mailing.message.topic,
                        message=mailing.message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email for client in mailing.clients.all()]
                    )
                    # Создание успешной попытки отправки
                    SendAttempt.objects.create(
                        datetime=current_datetime,
                        status=True,
                        response='Email sent successfully',
                        sending=mailing
                    )
                except Exception as e:
                    # Создание неудачной попытки отправки
                    SendAttempt.objects.create(
                        datetime=current_datetime,
                        status=False,
                        response=str(e),
                        sending=mailing
                    )
                    logger.error(f"Error sending email: {e}")

                # Обновление времени для следующей попытки на основе периодичности
                mailing.datetime = mailing.calculate_next_datetime()
                mailing.save()

            # Если количество отправленных писем достигает допустимого числа, изменить статус на "completed"
            if mailing.attempts.count() >= mailing.number_of_parcels:
                mailing.status = 'completed'
                mailing.save()

        # Ожидание указанного интервала перед следующей проверкой
        time.sleep(60)  # Проверка каждые 60 секунд