from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password

class SimpleSignupForm(UserCreationForm):
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput, strip=False)
    password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput, strip=False)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_password1(self):
        return self.cleaned_data.get("password1")
