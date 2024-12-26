from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.urls import reverse
from django.http import HttpResponseRedirect

from accounts.models import CustomUserModel
from accounts.forms import RegistrationForm
from accounts.checkers import send_otp, get_random_otp, otp_time_checker

from .models import Counseling, Session, Visit
from .forms import CounselingForm, SessionForm, VisitForm


# -------------------------------------- Counseling Views -------------------------------------- #
def counseling_view(request):
	if request.method == 'POST':
		form = CounselingForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('counseling_registration'))
	else:
		form = CounselingForm()
	return render(request, 'services/counseling.html', {'form': form})


def counseling_registration_view(request):
	form = RegistrationForm
	if request.method == 'POST':
		try:
			if 'phone_number' in request.POST:
				phone_number = request.POST.get('phone_number')
				user = CustomUserModel.objects.get(phone_number=phone_number)
				if user.otp_code is not None and otp_time_checker(user.phone_number):
					request.session['user_phone_number'] = user.phone_number
					return HttpResponseRedirect(reverse('counseling_verification'))
				otp = get_random_otp()
				send_otp(phone_number, otp)
				user.otp_code = otp
				user.save()
				request.session['user_phone_number'] = user.phone_number
				return HttpResponseRedirect(reverse('counseling_verification'))
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
				return HttpResponseRedirect(reverse('counseling_verification'))
	context = {
		'form': form,
	}
	return render(request, 'services/counseling_registration.html', context)


def counseling_verification_view(request):
	try:
		counseling = Counseling.objects.get(id=Counseling.objects.last().id)
		phone_number = request.session.get('user_phone_number')
		user = CustomUserModel.objects.get(phone_number=phone_number)
		if request.method == 'POST':
			if not otp_time_checker(user.phone_number) or user.otp_code != int(request.POST.get('otp')):
				return HttpResponseRedirect(reverse('counseling_registration'))
			user.is_active = True
			counseling.phone_number = user.phone_number
			counseling.save()
			user.save()
			login(request, user)
			return redirect('counseling_detail', pk=counseling.pk)
		context = {
			'phone_number': phone_number,
		}
		return render(request, 'services/counseling_verification.html', context)
	except CustomUserModel.DoesNotExist:
		return HttpResponseRedirect(reverse('counseling_registration'))


def counseling_detail(request, pk):
	counseling = get_object_or_404(Counseling, pk=pk)
	context = {
		'counseling': counseling,
	}
	return render(request, 'services/counseling_detail.html', context)


# -------------------------------------- Session Views  -------------------------------------- #
def session_view(request):
	if request.method == 'POST':
		form = SessionForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('session_registration'))
	else:
		form = SessionForm()
	return render(request, 'services/session.html', {'form': form})


def session_registration_view(request):
	form = RegistrationForm
	if request.method == 'POST':
		try:
			if 'phone_number' in request.POST:
				phone_number = request.POST.get('phone_number')
				user = CustomUserModel.objects.get(phone_number=phone_number)
				if user.otp_code is not None and otp_time_checker(user.phone_number):
					request.session['user_phone_number'] = user.phone_number
					return HttpResponseRedirect(reverse('session_verification'))
				otp = get_random_otp()
				send_otp(phone_number, otp)
				user.otp_code = otp
				user.save()
				request.session['user_phone_number'] = user.phone_number
				return HttpResponseRedirect(reverse('session_verification'))
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
				return HttpResponseRedirect(reverse('session_verification'))
	context = {
		'form': form,
	}
	return render(request, 'services/session_registration.html', context)


def session_verification_view(request):
	try:
		session = Session.objects.get(id=Session.objects.last().id)
		phone_number = request.session.get('user_phone_number')
		user = CustomUserModel.objects.get(phone_number=phone_number)
		if request.method == 'POST':
			if not otp_time_checker(user.phone_number) or user.otp_code != int(request.POST.get('otp')):
				return HttpResponseRedirect(reverse('session_registration'))
			user.is_active = True
			session.phone_number = user.phone_number
			session.save()
			user.save()
			login(request, user)
			return redirect('session_detail', pk=session.pk)
		context = {
			'phone_number': phone_number,
		}
		return render(request, 'services/session_verification.html', context)
	except CustomUserModel.DoesNotExist:
		return HttpResponseRedirect(reverse('session_registration'))


def session_detail(request, pk):
	session = get_object_or_404(Session, pk=pk)
	context = {
		'session': session,
	}
	return render(request, 'services/session_detail.html', context)


# -------------------------------------- Visit Views -------------------------------------- #
def visit_view(request):
	if request.method == 'POST':
		form = VisitForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('visit_registration'))
	else:
		form = VisitForm()
	return render(request, 'services/visit.html', {'form': form})


def visit_registration_view(request):
	form = RegistrationForm
	if request.method == 'POST':
		try:
			if 'phone_number' in request.POST:
				phone_number = request.POST.get('phone_number')
				user = CustomUserModel.objects.get(phone_number=phone_number)
				if user.otp_code is not None and otp_time_checker(user.phone_number):
					request.session['user_phone_number'] = user.phone_number
					return HttpResponseRedirect(reverse('visit_verification'))
				otp = get_random_otp()
				send_otp(phone_number, otp)
				user.otp_code = otp
				user.save()
				request.session['user_phone_number'] = user.phone_number
				return HttpResponseRedirect(reverse('visit_verification'))
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
				return HttpResponseRedirect(reverse('visit_verification'))
	context = {
		'form': form,
	}
	return render(request, 'services/visit_registration.html', context)


def visit_verification_view(request):
	try:
		visit = Visit.objects.get(id=Visit.objects.last().id)
		phone_number = request.session.get('user_phone_number')
		user = CustomUserModel.objects.get(phone_number=phone_number)
		if request.method == 'POST':
			if not otp_time_checker(user.phone_number) or user.otp_code != int(request.POST.get('otp')):
				return HttpResponseRedirect(reverse('visit_registration'))
			user.is_active = True
			visit.phone_number = user.phone_number
			visit.save()
			user.save()
			login(request, user)
			return redirect('visit_detail', pk=visit.pk)
		context = {
			'phone_number': phone_number,
		}
		return render(request, 'services/visit_verification.html', context)
	except CustomUserModel.DoesNotExist:
		return HttpResponseRedirect(reverse('visit_registration'))


def visit_detail(request, pk):
	visit = get_object_or_404(Visit, pk=pk)
	context = {
		'visit': visit,
	}
	return render(request, 'services/visit_detail.html', context)


