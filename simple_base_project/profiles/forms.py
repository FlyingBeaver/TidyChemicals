from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, min_length=1, label='Username:')
    password = forms.CharField(widget=forms.PasswordInput, label="Password:")
