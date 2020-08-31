from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

    

# The sign up form
class NewUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1']
        
class EditUserProfileForm(forms.ModelForm):
    """ This class is responsible for editing the details of the user """
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
        widgets = {
            'first_name': forms.TextInput(attrs = {
                'class': 'form-control form-control-sm ',
            }),
            'last_name': forms.TextInput(attrs = {
                'class': 'form-control form-control-sm ',
            }),
            'username': forms.TextInput(attrs = {
                'class': 'form-control form-control-sm ',
            }),
            'email': forms.EmailInput(attrs = {
                'class': 'form-control form-control-sm ',
            })
        }