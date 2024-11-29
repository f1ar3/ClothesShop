import re

from django import forms

class OrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    email = forms.CharField()
    delivery_address = forms.CharField(required=False)
    payment_by_card = forms.ChoiceField(
        choices=[
            ('0', False),
            ('1', True),
        ])

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError('The phone number must contains only numbers')

        pattern = re.compile(r'^\d{11}$')
        if not pattern.match(data):
            raise forms.ValidationError('Incorrect phone number format')

        return data
