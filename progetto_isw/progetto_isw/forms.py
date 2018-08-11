from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Username',
                   'required': 'true',
                   'autofocus': 'true'}))

    password = forms.CharField(
        label="Password",
        max_length=32,
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Password',
                   'required': 'true'}))


class SignupForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Username',
                   'required': 'true',
                   'autofocus': 'true'}))

    password = forms.CharField(
        label="Password",
        max_length=32,
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Password',
                   'required': 'true'}))

    password_confirm = forms.CharField(
        label="Repeat Password",
        max_length=32,
        widget=forms.PasswordInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Repeat Password',
                   'required': 'true'}))


class BoardCreationForm(forms.Form):
    board_name = forms.CharField(
        label="Board Name",
        max_length=512,
        required=True)


class ColumnCreationForm(forms.Form):
    column_name = forms.CharField(
        label="Column Name",
        max_length=512,
        required=True)
