from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



class LoginUser(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={"class":"form-control", "id":"email", "placeholder":"username"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class":"form-control", "id":"password", "placeholder":"Password", "autocomplete":"current-password"}))

    class Meta:
        model = User
        fields = ['email', 'password']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginUser, self).__init__(*args, **kwargs)

class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control mb-3", "required": True, "placeholder": "Username"})
        self.fields["email"].widget.attrs.update(
            {"class": "form-control mb-3", "required": True, "placeholder": "Email"})
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control mb-3", "required": True, "placeholder": "Password"})
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control mb-3", "required": True, "placeholder": "Confirm Password"})
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email address"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"

