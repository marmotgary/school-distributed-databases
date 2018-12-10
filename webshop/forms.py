from django.forms import ModelForm
from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name', 'address', 'country', 'post_code', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', max_length=4096, widget=forms.PasswordInput())
