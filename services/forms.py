from django import forms

from . import models


class CounselingForm(forms.ModelForm):
    class Meta:
        model = models.Counseling
        fields = ['city', 'counseling_type', 'date', 'time', 'name_and_family']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class SessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ['customer_type', 'trade_type', 'province', 'city', 'district',  'date', 'time', 'name_and_family']
        widgets = {
            'province': forms.Select(attrs={'id': 'province'}),
            'city': forms.Select(attrs={'id': 'city'}),
            'district': forms.Select(attrs={'id': 'district'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class VisitForm(forms.ModelForm):
    class Meta:
        model = models.Visit
        fields = ['province', 'city', 'district', 'date', 'time', 'name_and_family']
        widgets = {
            'province': forms.Select(attrs={'id': 'province'}),
            'city': forms.Select(attrs={'id': 'city'}),
            'district': forms.Select(attrs={'id': 'district'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


