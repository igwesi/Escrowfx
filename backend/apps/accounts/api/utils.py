import os
import threading
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template


class Utils:
    @staticmethod
    def send_mail(data):
        user = data['user']
        email = EmailMultiAlternatives(
            subject     = data['subject'],
            body        = data['body'],
            from_email  = settings.EMAIL_HOST_USER,
            to          = [user.email]
        )
        if data['template']:
            template = get_template(data['template'])
            html_content = template.render(data.get('context', {}))
            email.attach_alternative(html_content, "text/html")
            
        email.send(fail_silently=True)

    @staticmethod
    def send_mail_threaded(data):
        # Create a new thread for sending the email
        t = threading.Thread(target=Utils.send_mail, args=(data,))
        # Set the thread as a daemon to ensure it doesn't block the main process
        t.setDaemon(True)
        # Start the thread
        t.start()