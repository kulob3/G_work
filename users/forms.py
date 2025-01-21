from django import forms
from django.contrib.auth.forms import UserCreationForm
from sending.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'password1', 'password2']

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)