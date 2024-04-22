from django.db import models
from django.contrib.auth import get_user_model
from django_cryptography.fields import encrypt
User = get_user_model()


class BankAccount(models.Model):
    owner   = models.OneToOneField(User, on_delete=models.CASCADE)
    ngn_id  = encrypt(models.CharField(max_length=500, blank=True))
    usd_id  = encrypt(models.CharField(max_length=500, blank=True))    
    date_created = models.DateField(auto_now_add=True)    
    def __str__(self):
        return str(self.owner)



