from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField

from . import models, checkers


class AdminPanelUserCreateForm(UserCreationForm):
	class Meta:
		model = models.CustomUserModel
		fields = ('phone_number',)

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user


class AdminPanelUserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = models.CustomUserModel
		fields = ('phone_number', 'otp_code', 'is_verified', 'is_active', 'is_staff', 'is_superuser')

	def clean_password(self):
		return self.initial["password"]


class RegistrationForm(forms.ModelForm):
	class Meta:
		model = models.CustomUserModel
		fields = ['phone_number', 'otp_code']

	def clean(self):
		cleaned_data = super().clean()
		phone_number = cleaned_data.get('phone_number')
		otp_code = cleaned_data.get('otp_code')

		if phone_number and not checkers.phone_checker(phone_number):
			self.add_error('phone_number', 'شماره تلفن همراه وارد شده معتبر نیست.')
		if otp_code and not checkers.otp_checker(otp_code):
			self.add_error('otp_code', 'کد وارد شده معتبر نیست.')

		return cleaned_data


class AuthenticationForm(forms.ModelForm):
	class Meta:
		model = models.Profile
		fields = ['f_name', 'l_name', 'sex', 'national_code', 'email', 'province', 'city', 'address']
		widgets = {
			'address': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.required = True

	def clean(self):
		cleaned_data = super().clean()
		email = cleaned_data.get('email')
		national_code = cleaned_data.get('national_code')

		if email and not checkers.email_checker(email):
			self.add_error('email', 'ایمیل وارد شده معتبر نیست.')
		if national_code and not checkers.national_code_checker(national_code):
			self.add_error('national_code', 'کد ملی وارد شده معتبر نیست.')

		return cleaned_data


class InfoEditForm(forms.ModelForm):
	class Meta:
		model = models.Profile
		fields = ['email', 'province', 'city', 'address']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.required = True

	def clean(self):
		cleaned_data = super().clean()
		email = cleaned_data.get('email')
		national_code = cleaned_data.get('national_code')

		if email and not checkers.email_checker(email):
			self.add_error('email', 'ایمیل وارد شده معتبر نیست.')
		if national_code and not checkers.national_code_checker(national_code):
			self.add_error('national_code', 'کد ملی وارد شده معتبر نیست.')

		return cleaned_data



