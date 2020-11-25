from .models import BillingAddress
from django import forms

class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['first_name','last_name','company_name','state_or_country','town_or_city','phone','email','post_or_zipcode']
        widgets = {
            'first_name': forms.TextInput(attrs = {
                'class':'form-control',
                'required': True,
            }),
            'last_name': forms.TextInput(attrs = {
                'class':'form-control',
                'required': True,
            }),
            'company_name': forms.TextInput(attrs = {
                'class':'form-control'
            }),
            'state_or_country': forms.TextInput(attrs = {
                'class':'form-control',
                'required': True,
            }),
            'town_or_city': forms.TextInput(attrs = {
                'class':'form-control',
                'required': True,
            }),
            'phone': forms.TextInput(attrs = {
                'class':'form-control',
                'pattern':'^[+0]\d+$',
                'required': True,
            }),
            'email': forms.EmailInput(attrs = {
                'class':'form-control',
                'required': True,
            }),
            'post_or_zipcode': forms.TextInput(attrs = {
                'class':'form-control'
            }),
        }
