import random
import string

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext as _

from .managers import CustomUserManager
from services.models import Counseling, Session, Visit


# --------------------------------- Locations ---------------------------------
class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name


# --------------------------------- User ---------------------------------
class CustomUserModel(AbstractUser):
    IS_VERIFIED_CHOICES = [
        ('a', _('Authenticated')),
        ('n', _('Not Authenticated')),
        ('i', _('In Progress')),
    ]
    username = None
    phone_number = models.CharField(max_length=11, unique=True)
    otp_code = models.PositiveIntegerField(blank=True, null=True)
    otp_code_datetime_created = models.DateTimeField(auto_now=True)
    is_verified = models.CharField(max_length=10, choices=IS_VERIFIED_CHOICES, blank=True, null=True, default='n', verbose_name=_('Authentication Status'))

    objects = CustomUserManager()
    backend = 'accounts.backends.CustomAuthBackend'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    # Choices
    SEX_CHOICES = [
        ('m', _('Male')),
        ('f', _('Female')),
    ]
    INT_CHOICES = [
        ('ins', _('Instagram')),
        ('y&a', _('Course Videos')),
        ('ads', _('Advertisements')),
        ('web', _('Website and Google')),
        ('frd', _('Friends')),
        ('oth', _('Others')),
    ]
    # Fields
    f_name = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=_('First Name'))
    l_name = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=_('Last Name'))
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True, verbose_name=_('Sex'))
    national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('National Code'))
    email = models.CharField(max_length=300, blank=True, null=True, verbose_name=_('Email'))
    province = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Province'))
    city = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('City'))
    address = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_('Address'))
    introduction_way = models.CharField(max_length=10, choices=INT_CHOICES, blank=True, null=True, verbose_name=_('Introduction Way'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)


# --------------------------------- Tasks ---------------------------------
def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


def generate_unique_code():
    return ''.join(random.choices(string.digits + string.digits, k=6))


class Task(models.Model):
    TYPE_CHOICES = [
        ('cns', _('Counseling')),
        ('ses', _('Session')),
        ('vis', _('Visit')),
    ]
    PAYMENT_CHOICES = [
        ('yes', _('Yes')),
        ('no', _('No')),
    ]
    STATUS_CHOICES = [
        ('tkn', _('Taken')),
        ('fre', _('Free')),
        ('pen', _('Pending')),
    ]
    task_counseling = models.ForeignKey(Counseling, on_delete=models.CASCADE, related_name='counseling_task', blank=True, null=True)
    task_session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_task', blank=True, null=True)
    task_visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='visit_task', blank=True, null=True)
    type = models.CharField(max_length=6, choices=TYPE_CHOICES, null=True, blank=True, verbose_name=_('Task Type'))
    is_paid = models.CharField(max_length=10, choices=PAYMENT_CHOICES, blank=True, null=True, default='no', verbose_name=_('Payment Status'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True, default='fre', verbose_name=_('Request Status'))
    code = models.CharField(max_length=6, null=True, unique=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date and Time of Creation'))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_unique_code()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.code} / {self.type}'

    class Meta:
        ordering = ('-datetime_created',)



