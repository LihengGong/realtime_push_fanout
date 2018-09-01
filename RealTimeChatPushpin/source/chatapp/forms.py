from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    first_password = forms.CharField(widget=forms.PasswordInput,
                                     label='password')
    second_password = forms.CharField(widget=forms.PasswordInput,
                                      label='repeat password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_second_password(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['first_password'] != cleaned_data['second_password']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cleaned_data['second_password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    room = forms.CharField(max_length=30, initial='default')


class MessageForm(forms.Form):
    message = forms.CharField(max_length=100,
                              widget=forms.TextInput(attrs={'cols': 100, 'size': 200}))
