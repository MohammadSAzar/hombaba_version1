from django import forms

from . import models, checkers


counseling_required_fields = ['counseling_type', 'date', 'time', 'name_and_family']


class CounselingForm(forms.ModelForm):
    class Meta:
        model = models.Counseling
        fields = ['city', 'counseling_type', 'date', 'time', 'name_and_family']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'] = forms.ChoiceField(
            choices=models.next_seven_days_shamsi(),
            required=True,
            label=self.fields['date'].label,
        )
        for field in counseling_required_fields:
            self.fields[field].required = True

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        counseling_type = cleaned_data.get('counseling_type')
        name_and_family = cleaned_data.get('name_and_family')

        if not city and counseling_type == 'ip':
            self.add_error('city', 'انتخاب این فیلد برای مشاوره حضوری الزامی است')
        if name_and_family and not checkers.name_checker(name_and_family):
            self.add_error('name_and_family', 'فرمت نام و نام خانوادگی صحیح نیست')


class SessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ['customer_type', 'trade_type', 'province', 'city', 'district', 'date', 'time', 'name_and_family']
        widgets = {
            'province': forms.Select(attrs={'id': 'province'}),
            'city': forms.Select(attrs={'id': 'city'}),
            'district': forms.Select(attrs={'id': 'district'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'] = forms.ChoiceField(
            choices=models.next_seven_days_shamsi(),
            required=True,
            label=self.fields['date'].label,
        )
        for field in self.fields.values():
            field.required = True

    def clean(self):
        cleaned_data = super().clean()
        name_and_family = cleaned_data.get('name_and_family')

        if name_and_family and not checkers.name_checker(name_and_family):
            self.add_error('name_and_family', 'فرمت نام و نام خانوادگی صحیح نیست')


class VisitForm(forms.ModelForm):
    class Meta:
        model = models.Visit
        fields = ['trade_type', 'province', 'city', 'district', 'date', 'time', 'name_and_family']
        widgets = {
            'province': forms.Select(attrs={'id': 'province'}),
            'city': forms.Select(attrs={'id': 'city'}),
            'district': forms.Select(attrs={'id': 'district'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'] = forms.ChoiceField(
            choices=models.next_seven_days_shamsi(),
            required=True,
            label=self.fields['date'].label,
        )
        for field in self.fields.values():
            field.required = True

    def clean(self):
        cleaned_data = super().clean()
        name_and_family = cleaned_data.get('name_and_family')

        if name_and_family and not checkers.name_checker(name_and_family):
            self.add_error('name_and_family', 'فرمت نام و نام خانوادگی صحیح نیست')



