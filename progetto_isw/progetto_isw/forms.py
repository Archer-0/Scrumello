from django import forms
from models import Board, Column, Card


class LoginForm(forms.Form):
    login_username = forms.CharField(
        label="Username",
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Username',
                   'required': 'true',
                   'autofocus': 'true'})
    )

    login_password = forms.CharField(
        label="Password",
        max_length=32,
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Password',
                   'required': 'true'})
    )


class SignupForm(forms.Form):
    signup_username = forms.CharField(
        label="Username",
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Username',
                   'required': 'true',
                   'autofocus': 'true'})
    )

    signup_password = forms.CharField(
        label="Password",
        max_length=32,
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Password',
                   'required': 'true'})
    )

    signup_password_confirm = forms.CharField(
        label="Repeat Password",
        max_length=32,
        widget=forms.PasswordInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Repeat Password',
                   'required': 'true'})
    )


class BoardCreationForm(forms.Form):
    board_name = forms.CharField(
        label="Board Name",
        max_length=512,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form_popup_field-input',
                   'placeholder': 'New board name',
                   'required': 'true',
                   'autofocus': 'true'})
    )


class ColumnCreationForm(forms.Form):
    column_name = forms.CharField(
        label="Column Name",
        max_length=512,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'new_column-title',
                   'placeholder': '+ New Column',
                   'title': 'New Column Name',
                   'onkeyup': 'show_button(this)'})
    )
