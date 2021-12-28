from django import forms
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.Form):
    username = forms.CharField(label=False)
    email = forms.CharField(widget=forms.EmailInput, label=False)
    password = forms.CharField(widget=forms.PasswordInput, label=False)
    password_repeat = forms.CharField(widget=forms.PasswordInput, label=False)
    avatar = forms.FileField(required=False, label=False)


class SignUpForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput, label=False)
    username = forms.CharField(label=False)
    password1 = forms.CharField(widget=forms.PasswordInput, label=False)
    password2 = forms.CharField(widget=forms.PasswordInput, label=False)
    avatar = forms.FileField(required=False, label=False)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            self.add_error(None, "Passwords don`t match!")
        return cleaned_data


class AnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea(attrs={'rows':10}), label=False)


class QuestionForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput, label=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':10}), label=False)
    tag = forms.CharField(widget=forms.TextInput, label=False)


