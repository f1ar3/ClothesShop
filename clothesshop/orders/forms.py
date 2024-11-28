from django import forms

class OrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    email = forms.CharField()
    delivery_address = forms.CharField()
    payment_on_get = forms.ChoiceField(
        choices=[
            ('0', False),
            ('1', True),
        ])
