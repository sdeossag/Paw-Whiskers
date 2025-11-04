from django.utils.translation import gettext as _
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_("Correo electrónico"))

    class Meta:
        model = User
        fields = [_("username"), _("email"), _("password1"), _("password2")]

class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Usuario"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Contraseña"))