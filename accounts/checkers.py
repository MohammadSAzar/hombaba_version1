from kavenegar import *

from random import randint
import datetime
import time
import re

from config.settings import kavenegar_API
from .models import CustomUserModel


def send_otp(phone_number, otp):
    time.sleep(2)
    phone_number = [phone_number, ]
    try:
        api = KavenegarAPI(kavenegar_API)
        params = {
            'receptor': phone_number,
            'template': 'PhoneLoginTest',
            'token': f'{otp}',
            # 'token2': 'لاگین آزمایشی هومبیا',
            # 'token3': '',
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def get_random_otp():
    return randint(10000, 99999)


def otp_time_checker(phone_number):
    try:
        user = CustomUserModel.objects.get(phone_number=phone_number)
        now_time = datetime.datetime.now()
        otp_time = user.otp_code_datetime_created
        diff_time = now_time - otp_time
        print('DIFF TIME: ', diff_time)
        if diff_time.seconds > 30:  # better: 120
            return False
        return True
    except CustomUserModel.DoesNotExist:
        return False


def phone_checker(phone):
    try:
        if len(phone) == 11 and int(phone) and phone[0:2] == '09' and phone[2] in ['0', '1', '2', '3']:
            return True
    except ValueError:
        return False


def otp_checker(otp):
    try:
        if len(otp) == 5 and int(otp):
            return True
    except ValueError:
        return False


email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def email_checker(email):
    if re.fullmatch(email_regex, email):
        return True
    return False


def national_code_checker(code):
    try:
        if len(code) == 10 and int(code):
            number = 0
            for i in range(1, len(code)):
                number += (i + 1) * int(code[-(i + 1)])

            if number % 11 >= 2:
                control = 11 - number % 11
            else:
                control = number % 11

            if control == int(code[9]):
                return True
            else:
                return False

    except ValueError:
        return False


