import os
import threading
from django.conf import settings
from django.core.mail import EmailMessage


class Utils:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject     = data['subject'],
            body        = data['body'],
            from_email  = settings.EMAIL_HOST_USER,
            to          = [data['to_email']]
        )
        email.send()

    @staticmethod
    def send_mail_threaded(data):
        # Create a new thread for sending the email
        t = threading.Thread(target=Utils.send_mail, args=(data,))
        # Set the thread as a daemon to ensure it doesn't block the main process
        t.setDaemon(True)
        # Start the thread
        t.start()