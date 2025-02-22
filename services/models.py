import random
import string

from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _

from jdatetime import date, timedelta


# --------------------------------- Needs ---------------------------------
# covered cities
cities = [
    ('teh', _('Tehran')),
    ('krj', _('Karaj')),
]

# customer types
customer_types = [
    ('ol', _('Owner / Lessor')),
    ('bt', _('Buyer / Tenant')),
]

# day times
times = [
    ('mg', _('Morning')),
    ('nn', _('Noon')),
    ('eg', _('Evening')),
    ('nt', _('Night')),
]

# prices
counseling_price_value = 500000
session_price_value = 500000
visit_price_value = 500000


def next_seven_days_shamsi():
    days = []
    today = date.today()
    for i in range(1, 8):
        next_day = today + timedelta(days=i)
        days.append({
            'result_day': next_day.strftime('%A'),
            'result_date': next_day.strftime('%Y/%m/%d')
        })
    for j in range(0, 7):
        if days[j]['result_day'] == 'Monday' or days[j]['result_day'] == 'monday':
            days[j]['result_day'] = 'دوشنبه'
        if days[j]['result_day'] == 'Tuesday' or days[j]['result_day'] == 'tuesday':
            days[j]['result_day'] = 'سه‌شنبه'
        if days[j]['result_day'] == 'Wednesday' or days[j]['result_day'] == 'wednesday':
            days[j]['result_day'] = 'چهارشنبه'
        if days[j]['result_day'] == 'Thursday' or days[j]['result_day'] == 'thursday':
            days[j]['result_day'] = 'پنج‌شنبه'
        if days[j]['result_day'] == 'Friday' or days[j]['result_day'] == 'friday':
            days[j]['result_day'] = 'جمعه'
        if days[j]['result_day'] == 'Saturday' or days[j]['result_day'] == 'saturday':
            days[j]['result_day'] = 'شنبه'
        if days[j]['result_day'] == 'Sunday' or days[j]['result_day'] == 'sunday':
            days[j]['result_day'] = 'یکشنبه'
    final_days = []
    for k in range(0, 7):
        converted_day = str(days[k]['result_day'] + ' - ' + days[k]['result_date'])
        final_days.append((
            'result_day', converted_day,
        ))
    return final_days


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


class District(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts')
    price_session = models.PositiveBigIntegerField(verbose_name=_('Session Price'))
    price_visit = models.PositiveBigIntegerField(verbose_name=_('Visit Price'))

    def __str__(self):
        return self.name


# --------------------------------- Services ---------------------------------
class Counseling(models.Model):
    # Constants
    COUNSELING_TYPES = [
        ('ip', _('In Person')),
        ('op', _('On Phone')),
        ('oc', _('On Chat')),
    ]
    CUSTOMER_TYPES = customer_types
    DATES = next_seven_days_shamsi
    TIMES = times
    # Fields
    city = models.CharField(max_length=30, default=_('Tehran'), blank=True, null=True, verbose_name=_('City'))
    counseling_type = models.CharField(max_length=30, default='oc', choices=COUNSELING_TYPES, verbose_name=_('Counseling Type'))
    date = models.CharField(max_length=200, choices=DATES, verbose_name=_('Date of Counseling'))
    time = models.CharField(max_length=200, choices=TIMES, verbose_name=_('Time of Counseling'))
    name_and_family = models.CharField(max_length=200, verbose_name=_('Name and Family'))
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('Phone Number'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date and Time of Creation'))

    @property
    def price(self):
        price = counseling_price_value
        return price

    @property
    def tax(self):
        tax = int(counseling_price_value * 0.1)
        return tax

    @property
    def price_plus_tax(self):
        price_plus_tax = int(counseling_price_value + counseling_price_value * 0.1)
        return price_plus_tax

    @property
    def tracking_code(self):
        number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        choice_list = list(string.ascii_lowercase) + number_list + number_list
        code = ''
        for i in range(19):
            code = code + random.choice(choice_list)
        return code

    def get_absolute_url(self):
        return reverse('counseling_detail', args=[self.id])


class Session(models.Model):
    # Constants
    CITIES = cities
    CUSTOMER_TYPES = customer_types
    DATES = next_seven_days_shamsi
    TIMES = times
    # Locations
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions', verbose_name=_('Province'))
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions', verbose_name=_('City'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions', verbose_name=_('District'))
    # Fields
    customer_type = models.CharField(max_length=30, choices=CUSTOMER_TYPES, verbose_name=_('Customer Type'))
    date = models.CharField(max_length=200, choices=DATES, verbose_name=_('Date of Session'))
    time = models.CharField(max_length=200, choices=TIMES, verbose_name=_('Time of Session'))
    name_and_family = models.CharField(max_length=200, verbose_name=_('Name and Family'))
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('Phone Number'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date and Time of Creation'))

    @property
    def price(self):
        price = session_price_value
        return price

    @property
    def tax(self):
        tax = int(session_price_value * 0.1)
        return tax

    @property
    def price_plus_tax(self):
        price_plus_tax = int(session_price_value + session_price_value * 0.1)
        return price_plus_tax

    @property
    def tracking_code(self):
        number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        choice_list = list(string.ascii_lowercase) + number_list + number_list
        code = ''
        for i in range(19):
            code = code + random.choice(choice_list)
        return code

    def get_absolute_url(self):
        return reverse('session_detail', args=[self.id])


class Visit(models.Model):
    # Constants
    CITIES = cities
    DATES = next_seven_days_shamsi
    TIMES = times
    # Locations
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name='visits', verbose_name=_('Province'))
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='visits', verbose_name=_('City'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='visits', verbose_name=_('District'))
    # Fields
    date = models.CharField(max_length=200, choices=DATES, verbose_name=_('Date of Visit'))
    time = models.CharField(max_length=200, choices=TIMES, verbose_name=_('Time of Visit'))
    name_and_family = models.CharField(max_length=200, verbose_name=_('Name and Family'))
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('Phone Number'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date and Time of Creation'))

    @property
    def price(self):
        price = visit_price_value
        return price

    @property
    def tax(self):
        tax = int(visit_price_value * 0.1)
        return tax

    @property
    def price_plus_tax(self):
        price_plus_tax = int(visit_price_value + visit_price_value*0.1)
        return price_plus_tax

    @property
    def tracking_code(self):
        number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        choice_list = list(string.ascii_lowercase) + number_list + number_list
        code = ''
        for i in range(19):
            code = code + random.choice(choice_list)
        return code

    def get_absolute_url(self):
        return reverse('visit_detail', args=[self.id])



