from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .api.utils import Utils


def email_new_user(sender, instance, created, **kwargs):
    if created: # Check if the user was just created
        data = {
            'user':instance,
            'subject':'New Account Creation',
            'body':f'New Account has been created with {instance.email}',
            'template':'accounts/email/new_account_notification.html',
        }
        Utils.send_mail_threaded(data)
        
post_save.connect(email_new_user, sender=User)
