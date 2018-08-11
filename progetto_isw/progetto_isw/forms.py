from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=32, required=True)
    password = forms.CharField(label="Password", max_length=32, required=True, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(label="Username", max_length=32, required=True)
    password = forms.CharField(label="Password", max_length=32, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Repeat Password", max_length=32, required=True, widget=forms.PasswordInput)


class BoardCreationForm(forms.Form):
    name = forms.CharField(label="Board Name", max_length=512, required=True)


class ColumnCreationForm(forms.Form):
    name = forms.CharField(label="Column Name", max_length=512, required=True)

