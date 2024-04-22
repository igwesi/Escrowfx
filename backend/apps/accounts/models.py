import re
import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django_cryptography.fields import encrypt


COUNTRY = (
    ("AU", "Australia"),
    ("CA", "Canada"),
    ("GH", "Ghana"),
    ("NG", "Nigeria"),
    ("US", "United States"),    
)

class UserManager(BaseUserManager):
    def __create_user(self, email, username, tel, password=None):
        if not email:
            raise ValueError("User must provide a valid email address")
        if not username:
            raise ValueError("User must provide a username")
        if not tel:
            raise ValueError("User must provide a phone number")
                
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            tel=tel
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, username, tel, password):
        user = self.__create_user(email, username, tel, password)
        return user
    
    def create_superuser(self, email, username, tel, password):
        user = self.__create_user(email, username, tel, password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_verified = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id         = models.CharField(max_length=200, unique=True, primary_key=True, editable=False)
    person_id       = encrypt(models.CharField(max_length=200, blank=True))
    business_id     = encrypt(models.CharField(max_length=200, blank=True))
    
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    email           = models.EmailField(unique=True)
    username        = models.CharField(unique=True, max_length=50)
    tel             = PhoneNumberField()
    dob             = models.DateField(verbose_name="Date of Birth", default='1900-01-01')    
    
    business_name   = models.CharField(max_length=50, blank=True)
    role            = models.CharField(max_length=50, help_text="CEO, CFO", blank=True)    
    
    # User's Address Section: All Fields are Required
    zip_code        = models.IntegerField(verbose_name="Zip Code", null=True)
    address_line    = models.CharField(max_length=200, verbose_name="Address House no and street")
    city            = models.CharField(max_length=50, verbose_name="Address City")
    state           = models.CharField(max_length=50, verbose_name="Address State")
    country         = models.CharField(max_length=50, verbose_name="Country Codes e.g US, NG", choices=COUNTRY)
    
    # kyc_status      = models.CharField(max_length=20, choices=(
    #     ("Pending", "Pending"),
    #     ("submitted", "submitted"),
    #     ("Approved", "Approved"),
    #     ("Rejected", "Rejected")),
    #     default="Pending"
    # )
    
    # User's Permissions Section
    is_active       = models.BooleanField(default=True)
    is_verified     = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD  = 'email'
    EMAIL_FIELD     = 'email'
    USER_ID_FIELD   = 'user_id'
    REQUIRED_FIELDS = ['username','tel']
    
    # Objects used for creating a user
    objects = UserManager()
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = str(uuid.uuid4()).replace("-","")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.user_id)
    
    def get_dob(self):
        dob = self.dob.strftime("%Y-%m-%d")
        return dob
    
    def get_tel(self):
        phone = str(self.tel.raw_input).replace('+','')
        return phone
    def has_perm(self, perm, obj=None):
        return True    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
