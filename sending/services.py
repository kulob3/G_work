import time
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
import pytz
from sending.models import Sending, SendAttempt

def send_mailing(pytz=pytz):
    print("Рассылки запущены")
    while True:
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)

        # Filter mailings based on datetime and status "started"
        mailings = Sending.objects.filter(
            datetime__lte=current_datetime,
            status='started'
        )

        for mailing in mailings:
            # Check if the number of emails sent is less than the allowed number
            if mailing.attempts.count() < mailing.number_of_parcels:
                try:
                    send_mail(
                        subject=mailing.message.topic,
                        message=mailing.message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email for client in mailing.clients.all()]
                    )
                    # Create a successful send attempt
                    SendAttempt.objects.create(
                        datetime=current_datetime,
                        status=True,
                        response='Email sent successfully',
                        sending=mailing
                    )
                except Exception as e:
                    # Create a failed send attempt
                    SendAttempt.objects.create(
                        datetime=current_datetime,
                        status=False,
                        response=str(e),
                        sending=mailing
                    )
                # Update the datetime for the next attempt based on periodicity
                mailing.datetime = mailing.calculate_next_datetime()
                mailing.save()

            # If the number of emails sent reaches the allowed number, change status to "completed"
            if mailing.attempts.count() >= mailing.number_of_parcels:
                mailing.status = 'completed'
                mailing.save()

        # Wait for a specified interval before checking again
        time.sleep(60)  # Check every 60 seconds