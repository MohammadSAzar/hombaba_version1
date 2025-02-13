from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render


from .models import CustomUserModel, Profile, Task
from .forms import RegistrationForm, AuthenticationForm, InfoEditForm
from .checkers import send_otp, get_random_otp, otp_time_checker

from services.models import Counseling, Session, Visit


# def not_logged_in(user):
#     return not user.is_authenticated


# @user_passes_test(not_logged_in, login_url='/verification')
def registration_view(request):
    form = RegistrationForm
    if request.method == 'POST':
        try:
            if 'phone_number' in request.POST:
                phone_number = request.POST.get('phone_number')
                user = CustomUserModel.objects.get(phone_number=phone_number)
                if user.otp_code is not None and otp_time_checker(user.phone_number):
                    request.session['user_phone_number'] = user.phone_number
                    return HttpResponseRedirect(reverse('verification'))
                otp = get_random_otp()
                send_otp(phone_number, otp)
                user.otp_code = otp
                user.save()
                request.session['user_phone_number'] = user.phone_number
                return HttpResponseRedirect(reverse('verification'))
        except CustomUserModel.DoesNotExist:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                otp = get_random_otp()
                send_otp(phone_number, otp)
                user.otp_code = otp
                user.is_active = False
                user.save()
                request.session['user_phone_number'] = user.phone_number
                return HttpResponseRedirect(reverse('verification'))
    context = {
        'form': form,
    }
    if request.user.is_authenticated:
        raise PermissionDenied
    return render(request, 'accounts/registration.html', context)


# @user_passes_test(not_logged_in, login_url='/profile_info_now')
def verification_view(request):
    try:
        phone_number = request.session.get('user_phone_number')
        user = CustomUserModel.objects.get(phone_number=phone_number)
        if request.method == 'POST':
            if not otp_time_checker(user.phone_number) or user.otp_code != int(request.POST.get('otp')):
                return HttpResponseRedirect(reverse('verification'))
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('profile_info_now'))
        context = {
            'phone_number': phone_number,
        }
        if request.user.is_authenticated:
            raise PermissionDenied
        return render(request, 'accounts/verification.html', context)
    except CustomUserModel.DoesNotExist:
        return HttpResponseRedirect(reverse('registration'))


# --------------------------------- Profile ---------------------------------
# @login_required(login_url='/login')
def profile_info_now_view(request):
    context = {}
    phone_number = request.session.get('user_phone_number')
    if phone_number:
        user = CustomUserModel.objects.get(phone_number=phone_number)
        context['user'] = user
    else:
        user = request.user
        context['user'] = user
    if not request.user.is_authenticated:
        raise PermissionDenied
    return render(request, 'accounts/profile_info_now.html', context)


# @login_required(login_url='/login')
def profile_info_auth_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            profile = form.save(commit=False)
            # profile.user = user
            profile.save()
            user.profile = profile
            form.save()
            user.is_verified = 'i'
            user.save()
            messages.success(request, "اطلاعات شما دریافت شد، نتیجه فرایند احراز هویت بزودی تعیین می‌شود.")
            return HttpResponseRedirect(reverse('profile_info_now'))
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    if not request.user.is_authenticated:
        raise PermissionDenied
    return render(request, 'accounts/profile_info_auth.html', context)


# @login_required(login_url='/login')
def profile_info_edit_view(request):
    if request.method == 'POST':
        form = InfoEditForm(request.POST)
        user = request.user
        profile = Profile.objects.get(user=user)
        if form.is_valid():
            form.save()
            profile.save()
            messages.success(request, "اطلاعات شما با موفقیت اصلاح شد.")
            return HttpResponseRedirect(reverse('profile_info_now'))
    else:
        form = InfoEditForm()
    context = {
        'form': form,
    }
    if not request.user.is_authenticated:
        raise PermissionDenied
    return render(request, 'accounts/profile_info_edit.html', context)


# @login_required(login_url='/login')
def profile_your_services_view(request):
    phone_number = request.session.get('user_phone_number')
    counselings = Counseling.objects.filter(phone_number=phone_number).all()
    sessions = Session.objects.filter(phone_number=phone_number).all()
    visits = Visit.objects.filter(phone_number=phone_number).all()
    context = {
        'counselings': counselings,
        'sessions': sessions,
        'visits': visits,
    }
    if not request.user.is_authenticated:
        raise PermissionDenied
    return render(request, 'accounts/profile_your_services.html', context)


