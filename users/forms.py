from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError

from users.models import User


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields =[
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()


class LoginUserForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']

class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields=[
            'image',
            'first_name',
            'last_name',
            'username',
            'email',
        ]
        image = forms.ImageField(required=False)
        first_name = forms.CharField(required=False)
        last_name = forms.CharField(required=False)
        username = forms.CharField()
        email = forms.CharField()





